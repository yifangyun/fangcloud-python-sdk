import json
import logging
import os
import random
import time

import requests
import six
import sys
from requests_toolbelt import MultipartEncoderMonitor

from fangcloud.exceptions import InternalServerError, RateLimitError, BadInputError, AuthError, YfyAPIException, DownloadError, TokenRefreshed
from fangcloud.oauth import FangcloudOAuth2FlowBase
from fangcloud.session import create_session
from fangcloud.system_info import YfySystemInfo


class Response(object):

    def __init__(self, raw, http_resp=None):
        """
        :param raw: The raw result, if one exists. Must be serialized JSON.
        :param http_resp: requests.models.Response http_resp: A raw HTTP response. It will
            be used to stream the binary-body payload of the response
        """
        if http_resp is not None:
            assert isinstance(http_resp, requests.models.Response), \
                'http_resp: expected requests.models.Response, got %r' % \
                type(http_resp)
        self.raw = raw
        self.http_resp = http_resp


class ErrorResponse(object):

    def __init__(self, request_id, status_code, raw):
        self.raw = raw
        self.request_id = request_id
        self.status_code = status_code


class YfyTransport(object):

    _API_VERSION = "V2"

    # This is the default longest time we'll block on receiving data from the server
    _DEFAULT_TIMEOUT = 30

    _DOWNLOAD_CHUNK_SIZE = 10240

    _ROUTE_STYLE_DOWNLOAD = 'download'
    _ROUTE_STYLE_UPLOAD = 'upload'
    _ROUTE_STYLE_RPC = 'rpc'

    _METHOD_GET = 'get'
    _METHOD_POST = 'post'

    _RESULT_TYPE_JSON = 'json'
    _RESULT_TYPE_RAW = 'raw'

    _session = create_session()

    def __init__(self,
                 oauth2_access_token,
                 oauth2_refresh_token,
                 call_back,
                 max_retries_on_error=2,
                 max_retries_on_rate_limit=None,
                 session=None,
                 headers=None,
                 proxy=None,
                 timeout=_DEFAULT_TIMEOUT):
        """
        :param str oauth2_access_token: OAuth2 access token for making client requests.
        :param str oauth2_refresh_token: OAuth2 refresh token for refresh oauth2 token
        :param Optional[int] max_retries_on_error: On 5xx errors, the number of times to retry.
        :param Optional[int] max_retries_on_rate_limit: On 429 errors, the number of times to retry. If `None`, always retries.
        :param session: If not provided, a new session (connection pool) is created. To share a session across multiple clients, use
            :func:`create_session`.
        :param dict headers: Additional headers to add to requests.
        :param dict proxy: Only http and https supported, json example.
            {
                'http': 'http://%s:%s@%s:%d' % (user_name, password, ip_address, port),
                'https': 'https://%s:%s@%s:%d' % (user_name, password, ip_address, port)
            }
        :param Optional[float] timeout: timeout: Maximum duration in seconds that client will wait for any single packet from the
            server. After the timeout the client will give up on connection. If `None`, client will wait forever. Defaults
            to 30 seconds.
        """
        assert len(oauth2_access_token) > 0, 'OAuth2 access token cannot be empty.'
        assert headers is None or isinstance(headers, dict), 'Expected dict, got %r' % headers
        self._oauth2_access_token = oauth2_access_token
        self._oauth2_refresh_token = oauth2_refresh_token
        self._max_retries_on_error = max_retries_on_error
        self._max_retries_on_rate_limit = max_retries_on_rate_limit
        self._user_agent = ''.join([YfySystemInfo.client_id, ' ', 'OfficialFangcloudPythonSDK', '/', YfySystemInfo.sdk_version])
        self._headers = headers
        self._timeout = timeout
        self._proxy = proxy
        self._call_back = call_back
        self._logger = logging.getLogger('yifangyun')

        if session:
            assert isinstance(session, requests.sessions.Session), \
                'Expected requests.sessions.Session, got %r' % session
            self._session = session

    def get(self, url, **kwargs):
        kwargs.setdefault('route_style', self._ROUTE_STYLE_RPC)
        return self.request_with_retry(self._METHOD_GET, url, **kwargs)

    def post(self, url, **kwargs):
        kwargs.setdefault('route_style', self._ROUTE_STYLE_RPC)
        return self.request_with_retry(self._METHOD_POST, url, **kwargs)

    def post_file(self, url, **kwargs):
        kwargs.setdefault('route_style', self._ROUTE_STYLE_UPLOAD)
        return self.request_with_retry(self._METHOD_POST, url, **kwargs)

    def get_file(self, url, file_path, **kwargs):
        kwargs.setdefault('route_style', self._ROUTE_STYLE_DOWNLOAD)
        kwargs.setdefault('result_type', self._RESULT_TYPE_RAW)
        raw, response = self.request_with_retry(self._METHOD_GET, url, **kwargs)

        try:
            # download file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self._DOWNLOAD_CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        except Exception as exception:
            raise DownloadError(response.status_code, str(exception))
        return raw

    def request_with_retry(self,
                           method,
                           url,
                           params=None,
                           route_style=None,
                           request_json_arg=None,
                           result_type=_RESULT_TYPE_JSON,
                           upload_file_path=None,
                           proxy=None,
                           timeout=None):
        attempt = 0
        rate_limit_errors = 0
        while True:
            self._logger.info('Requests to url = %s', url)
            try:
                result = self.send_request(method,
                                           url,
                                           params,
                                           route_style,
                                           request_json_arg,
                                           upload_file_path,
                                           proxy,
                                           timeout
                                           )
                if isinstance(result, Response):
                    if result_type == self._RESULT_TYPE_JSON:
                        return json.loads(result.raw)
                    elif result_type == self._RESULT_TYPE_RAW:
                        return result.raw, result.http_resp
                elif isinstance(result, ErrorResponse):
                    raise YfyAPIException(result.request_id, result.status_code, result.raw)
                else:
                    raise AssertionError('Expected Response or ErrorResponse, but res is %s' % type(result))

            except InternalServerError as e:
                attempt += 1
                if attempt <= self._max_retries_on_error:
                    # Use exponential back off
                    back_off = 2 ** attempt * random.random()
                    self._logger.info('HttpError status_code=%s: Retrying in %.1f seconds', e.status_code, back_off)
                    time.sleep(back_off)
                else:
                    raise
            except RateLimitError as e:
                rate_limit_errors += 1
                if (self._max_retries_on_rate_limit is None or
                        self._max_retries_on_rate_limit >= rate_limit_errors):
                    # Set default back off to 5 seconds.
                    back_off = e.back_off if e.back_off is not None else 5.0
                    self._logger.info('Rate limit: Retrying in %.1f seconds.', back_off)
                    time.sleep(back_off)
                else:
                    raise
            except TokenRefreshed as e:
                pass

    def send_request(self,
                     method,
                     url,
                     params,
                     route_style,
                     request_json_arg,
                     upload_file_path,
                     proxy,
                     timeout):
        headers = {
            'Authorization': 'Bearer %s' % self._oauth2_access_token,
            'X-Runtime-Version': sys.version.split(" ")[0]
        }

        if self._user_agent is not None:
            headers.update({'User-Agent': self._user_agent})

        if self._headers:
            headers.update(self._headers)

        if timeout is None:
            timeout = self._timeout

        if proxy is None:
            proxy = self._proxy

        # The contents of the body of the HTTP request
        stream = False
        if route_style == self._ROUTE_STYLE_RPC:
            headers['Content-Type'] = 'application/json'
            if self._API_VERSION == "V1":
                headers['Accept'] = 'application/v1+json'
            elif self._API_VERSION == "V2":
                headers['Accept'] = 'application/v2+json'
            else:
                headers['Accept'] = 'application/json'
            body = request_json_arg
            if method == self._METHOD_GET:
                r = self._session.get(url,
                                      headers=headers,
                                      params=params,
                                      stream=stream,
                                      verify=True,
                                      proxies=proxy,
                                      timeout=timeout
                                      )
            elif method == self._METHOD_POST:
                r = self._session.post(url,
                                       headers=headers,
                                       params=params,
                                       json=body,
                                       stream=stream,
                                       verify=True,
                                       proxies=proxy,
                                       timeout=timeout
                                       )
            else:
                raise ValueError('Unknown method: %r' % method)
        elif route_style == self._ROUTE_STYLE_DOWNLOAD:
            r = self._session.get(url,
                                  params=params,
                                  headers=headers,
                                  stream=True,
                                  verify=True,
                                  proxies=proxy,
                                  timeout=timeout
                                 )
        elif route_style == self._ROUTE_STYLE_UPLOAD:
            file_handler = open(upload_file_path, 'rb')
            files = {'file': ("yifangyun-file", file_handler, {'Expires': '0'})}
            multipart_monitor = MultipartEncoderMonitor.from_fields(fields=files)
            headers['Content-Type'] = multipart_monitor.content_type
            r = self._session.post(url,
                                   headers=headers,
                                   params=params,
                                   data=multipart_monitor,
                                   stream=stream,
                                   verify=True,
                                   proxies=proxy,
                                   timeout=timeout
                                   )
        else:
            raise ValueError('Unknown operation style: %r' % route_style)

        if 200 <= r.status_code <= 299:
            if route_style == self._ROUTE_STYLE_DOWNLOAD:
                raw_resp = True
            else:
                raw_resp = r.content.decode('utf-8')

            if route_style == self._ROUTE_STYLE_DOWNLOAD:
                return Response(raw_resp, r)
            else:
                return Response(raw_resp)
        else:
            response = r.json()
            request_id = response.get('request_id')
            assert request_id is not None, ('Expected request id in response, but cannot find in %r'%r.text)
            if r.status_code >= 500:
                raise InternalServerError(request_id, r.status_code, r.text)
            elif r.status_code == 400:
                raise BadInputError(request_id, r.status_code, r.text)
            elif r.status_code == 401:
                oauth2 = FangcloudOAuth2FlowBase(request_session=self._session, request_id=request_id)
                result = oauth2.refresh_token(self._oauth2_refresh_token)
                self._oauth2_access_token = result.access_token
                self._oauth2_refresh_token = result.refresh_token
                if self._call_back is not None:
                    self._call_back.on_token_refresh(result.access_token, result.refresh_token)
                raise TokenRefreshed(request_id)
            elif r.status_code == 429:
                err = None
                retry_after = r.headers.get('X-Rate-Limit-Reset')
                raise RateLimitError(request_id, err, int(retry_after))
            elif r.status_code in (403, 404, 409):
                raw_resp = r.content.decode('utf-8')
                return ErrorResponse(request_id, r.status_code, raw_resp)
            else:
                raise YfyAPIException(request_id, r.status_code, r.text)





