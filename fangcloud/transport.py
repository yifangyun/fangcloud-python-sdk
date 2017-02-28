import json
import logging
import random
import time

import requests
import six

from fangcloud.exceptions import InternalServerError, RateLimitError, BadInputError, AuthError, YfyAPIException
from fangcloud.session import create_session


class Response(object):

    def __init__(self, raw, http_resp=None):
        """
        :param raw: The raw result, if one exists. Must be serialized JSON.
        :param http_resp: requests.models.Response http_resp: A raw HTTP response. It will
            be used to stream the binary-body payload of the response
        """
        assert isinstance(raw, six.string_types), \
            'obj_result: expected string, got %r' % type(raw)
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

    _API_VERSION = "V1"

    # This is the default longest time we'll block on receiving data from the server
    _DEFAULT_TIMEOUT = 30

    _ROUTE_STYLE_DOWNLOAD = 'download'
    _ROUTE_STYLE_UPLOAD = 'upload'
    _ROUTE_STYLE_RPC = 'rpc'

    _METHOD_GET = 'get'
    _METHOD_POST = 'post'
    _METHOD_DELETE = 'delete'
    _METHOD_PUT = 'put'

    _RESULT_TYPE_JSON = 'json'
    _RESULT_TYPE_RAW = 'raw'

    _session = create_session()

    def __init__(self,
                 oauth2_access_token,
                 oauth2_refresh_token,
                 max_retries_on_error=2,
                 max_retries_on_rate_limit=None,
                 user_agent=None,
                 session=None,
                 headers=None,
                 timeout=_DEFAULT_TIMEOUT):
        assert len(oauth2_access_token) > 0, 'OAuth2 access token cannot be empty.'
        assert headers is None or isinstance(headers, dict), 'Expected dict, got %r' % headers
        self._oauth2_access_token = oauth2_access_token
        self._oauth2_refresh_token = oauth2_refresh_token
        self._max_retries_on_error = max_retries_on_error
        self._max_retries_on_rate_limit = max_retries_on_rate_limit
        self._user_agent = user_agent
        self._headers = headers
        self._timeout = timeout
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

    def delete(self, url, **kwargs):
        kwargs.setdefault('route_style', self._ROUTE_STYLE_RPC)
        return self.request_with_retry(self._METHOD_DELETE, url, **kwargs)

    def put(self, url, **kwargs):
        kwargs.setdefault('route_style', self._ROUTE_STYLE_RPC)
        return self.request_with_retry(self._METHOD_PUT, url, **kwargs)

    def request_with_retry(self,
                           method,
                           url,
                           params=None,
                           route_style=None,
                           request_json_arg=None,
                           result_type=_RESULT_TYPE_JSON,
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
                                           timeout
                                           )
                if isinstance(result, Response):
                    if result_type == self._RESULT_TYPE_JSON:
                        return json.loads(result.raw)
                    elif result_type == self._RESULT_TYPE_RAW:
                        return result.raw
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
                    self._logger.info('Ratelimit: Retrying in %.1f seconds.', back_off)
                    time.sleep(back_off)
                else:
                    raise

    def send_request(self,
                     method,
                     url,
                     params,
                     route_style,
                     request_json_arg,
                     timeout):
        headers = {
            'Authorization': 'Bearer %s' % self._oauth2_access_token
        }
        if self._user_agent is not None:
            headers = {'User-Agent': self._user_agent}
        if self._headers:
            headers.update(self._headers)

        # The contents of the body of the HTTP request
        body = None
        stream = False
        if route_style == self._ROUTE_STYLE_RPC:
            if self._API_VERSION == "V1":
                headers['Content-Type'] = 'application/json'
            else:
                headers['Content-Type'] = 'application/json'
            body = request_json_arg
        elif route_style == self._ROUTE_STYLE_DOWNLOAD:
            stream = True
        elif route_style == self._ROUTE_STYLE_UPLOAD:
            headers['Content-Type'] = 'application/octet-stream'
        else:
            raise ValueError('Unknown operation style: %r' % route_style)

        if timeout is None:
            timeout = self._timeout

        if method == self._METHOD_GET:
            r = self._session.get(url,
                                  headers=headers,
                                  params=params,
                                  stream=stream,
                                  verify=True,
                                  timeout=timeout
                                  )
        elif method == self._METHOD_POST:
            r = self._session.post(url,
                                   headers=headers,
                                   params=params,
                                   json=body,
                                   stream=stream,
                                   verify=True,
                                   timeout=timeout
                                   )
        elif method == self._METHOD_DELETE:
            r = self._session.delete(url,
                                     headers=headers,
                                     params=params,
                                     json=body,
                                     stream=stream,
                                     verify=True,
                                     timeout=timeout
                                    )
        elif method == self._METHOD_PUT:
            r = self._session.put(url,
                                  headers=headers,
                                  params=params,
                                  json=body,
                                  stream=stream,
                                  verify=True,
                                  timeout=timeout
                                 )
        else:
            raise ValueError('Unknown method: %r' % method)

        if 200 <= r.status_code <= 299:
            if route_style == self._ROUTE_STYLE_DOWNLOAD:
                raw_resp = r.headers['dropbox-api-result']
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
                raise AuthError(request_id)
            elif r.status_code == 429:
                err = None
                retry_after = r.headers.get('X-Rate-Limit-Reset')
                raise RateLimitError(request_id, err, int(retry_after))
            elif r.status_code in (403, 404, 409):
                raw_resp = r.content.decode('utf-8')
                return ErrorResponse(request_id, r.status_code, raw_resp)
            else:
                raise YfyAPIException(request_id, r.status_code, r.text)
