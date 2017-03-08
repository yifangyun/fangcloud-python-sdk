
class OAuthParamError(Exception):

    """All oauth param related errors"""
    def __init__(self, *args, **kwargs):
        pass


class OAuthCodeParamError(OAuthParamError):

    def __init__(self, *args, **kwargs):
        super(OAuthCodeParamError, self).__init__(*args, **kwargs)


class OAuthRedirectParamError(OAuthParamError):

    def __init__(self, *args, **kwargs):
        super(OAuthRedirectParamError, self).__init__(*args, **kwargs)


class YfyException(Exception):

    def __init__(self, *args, **kwargs):
        super(YfyException, self).__init__(*args, **kwargs)

    def __str__(self):
        return repr(self)


class YfyHttpException(YfyException):

    """All errors related to http requests an API request extend this, including network error"""
    def __init__(self, *args, **kwargs):
        # A request_id can be shared with Fangcloud Support to pinpoint the exact
        # request that returns an error.
        super(YfyHttpException, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'Http Exception'


class YfyAPIException(YfyHttpException):

    """All errors related to making an API request extend this."""
    def __init__(self, request_id, status_code, body):
        # A request_id can be shared with Fangcloud Support to pinpoint the exact
        # request that returns an error.
        super(YfyAPIException, self).__init__(status_code, body)
        self.request_id = request_id
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return 'API Exception (request id = %s)' % self.request_id


class InternalServerError(YfyAPIException):

    """Errors due to a problem on Server side."""
    def __repr__(self):
        return 'InternalServerError({!r}, {}, {!r})'.format(self.request_id, self.status_code, self.body)


class BadInputError(YfyAPIException):
    """Errors due to bad input parameters to an API Operation."""

    def __init__(self, request_id, status_code, message):
        super(BadInputError, self).__init__(request_id, status_code, message)
        self.message = message

    def __repr__(self):
        return 'BadInputError({!r}, {!r})'.format(self.request_id, self.message)


class DownloadError(YfyAPIException):

    def __init__(self, status_code, message):
        super(DownloadError, self).__init__("", status_code, message)
        self.message = message

    def __repr__(self):
        return 'DownloadError({!r}, {}, {!r})'.format(self.request_id, self.status_code, self.message)


class AuthError(YfyAPIException):
    """Errors due to invalid authentication credentials."""

    def __init__(self, request_id):
        super(AuthError, self).__init__(request_id, 401, None)

    def __repr__(self):
        return 'AuthError(request_id = {!r})'.format(self.request_id)


class RateLimitError(YfyAPIException):

    """Error caused by rate limiting. Request will be resend in back off related seconds"""
    def __init__(self, request_id, error=None, back_off=None):
        super(RateLimitError, self).__init__(request_id, 429, None)
        self.error = error
        self.back_off = back_off

    def __repr__(self):
        return 'RateLimitError (request_id = {!r}, error = {!r})'.format(self.request_id, self.error)


class TokenRefreshed(YfyAPIException):

    def __init__(self, request_id):
        super(TokenRefreshed, self).__init__(request_id, 200, None)
