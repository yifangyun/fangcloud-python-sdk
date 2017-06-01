
import os
import urllib

import six
from requests.auth import HTTPBasicAuth

from fangcloud.exceptions import OAuthCodeParamError, OAuthRedirectParamError, AuthError, InternalServerError, BadInputError
from fangcloud.session import pinned_session
from fangcloud.system_info import YfySystemInfo
from fangcloud.url_builder import UrlBuilder

if six.PY3:
    url_path_quote = urllib.parse.quote
    url_encode = urllib.parse.urlencode
else:
    url_path_quote = urllib.quote
    url_encode = urllib.urlencode


def _params_to_urlencoded(params):
    def encode(o):
        if isinstance(o, six.binary_type):
            return o
        else:
            if isinstance(o, six.text_type):
                return o.encode('utf-8')
            else:
                return str(o).encode('utf-8')

    utf8_params = {encode(k): encode(v) for k, v in six.iteritems(params)}
    return url_encode(utf8_params)


class OAuth2FlowNoRedirectResult(object):
    """
    Authorization information for an OAuth2Flow performed with no redirect.
    """

    def __init__(self, access_token, refresh_token, expires_in):
        """
        :param access_token: Token to be used to authenticate later requests.
        :param refresh_token: Refresh access token when access token expired.
        :param expires_in: Access token expired time.
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

    def __repr__(self):
        return 'OAuth2FlowNoRedirectResult(access_token=%r, refresh_token=%r, expires_in=%r)' % (
            self.access_token,
            self.refresh_token,
            self.expires_in,
        )


class FangcloudOAuth2FlowBase(object):

    def __init__(self, locale=None, request_session=None, request_id=None):
        assert YfySystemInfo.get_client_id() is not None
        assert YfySystemInfo.get_client_secret() is not None
        self.client_id = YfySystemInfo.get_client_id()
        self.client_secret = YfySystemInfo.get_client_secret()
        self.locale = locale
        self.request_id = request_id
        if request_session is None:
            self.requests_session = pinned_session()
        else:
            self.requests_session = request_session
        self._host = UrlBuilder.get_oauth_host()

    def get_authorize_url(self, redirect_uri, state):
        query_params = dict(
            response_type='code',
            client_id=self.client_id
        )

        if redirect_uri is not None:
            query_params['redirect_uri'] = redirect_uri
        if state is not None:
            query_params['state'] = state

        return self.build_url('/oauth/authorize', query_params)

    def authenticate(self, code, redirect_uri):
        if code is None or redirect_uri is None:
            raise OAuthCodeParamError

        if redirect_uri is None:
            raise OAuthRedirectParamError

        url = self.build_url('/oauth/token')
        params = {
                    'grant_type': 'authorization_code',
                    'code': code,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                  }
        if self.locale is not None:
            params['locale'] = self.locale
        if redirect_uri is not None:
            params['redirect_uri'] = redirect_uri

        resp = self.requests_session.post(url, data=params, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        resp.raise_for_status()
        result = resp.json()
        return OAuth2FlowNoRedirectResult(
            result['access_token'],
            result['refresh_token'],
            result.get('expires_in', None)  # none if never expires
        )

    def password_login(self, user_name, password):
        if user_name is None or password is None:
            raise AuthError(self.request_id)

        url = self.build_url('/oauth/token')
        params = {
            'grant_type': 'password',
            'username': user_name,
            'password': password
        }
        resp = self.requests_session.post(url, data=params, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        result = resp.json()

        if resp.status_code >= 500:
            raise InternalServerError(self.request_id, resp.status_code, resp.text)
        elif resp.status_code == 400:
            raise BadInputError(self.request_id, resp.status_code, resp.text)
        elif resp.status_code == 200:
            return OAuth2FlowNoRedirectResult(
                result['access_token'],
                result['refresh_token'],
                result.get('expires_in', None)
            )
        else:
            raise AuthError(self.request_id)

    def refresh_token(self, refresh_token):
        if refresh_token is None:
            raise AuthError(self.request_id)

        url = self.build_url('/oauth/token')
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        resp = self.requests_session.post(url, data=params, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        result = resp.json()

        if resp.status_code >= 500:
            raise InternalServerError(self.request_id, resp.status_code, resp.text)
        elif resp.status_code == 400:
            raise BadInputError(self.request_id, resp.status_code, resp.text)
        elif resp.status_code == 200:
            return OAuth2FlowNoRedirectResult(
                result['access_token'],
                result['refresh_token'],
                result.get('expires_in', None)  # none if never expires
            )
        else:
            raise AuthError(self.request_id)

    def build_url(self, target, params=None):
        return "%s%s" % (self._host, self.build_path(target, params))

    def build_path(self, target, params=None):
        if six.PY2 and isinstance(target, six.text_type):
            target = target.encode('utf8')

        target_path = url_path_quote(target)

        params = params or {}
        params = params.copy()

        if self.locale:
            params['locale'] = self.locale

        if params:
            query_string = _params_to_urlencoded(params)
            return "%s?%s" % (target_path, query_string)
        else:
            return "%s" % target_path








