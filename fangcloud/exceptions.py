
class OAuthParamError(Exception):
    """All oauth param related errors"""
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class OAuthCodeParamError(OAuthParamError):
    def __init__(self, *args, **kwargs): # real signature unknown
        super(OAuthCodeParamError, self).__init__(*args, **kwargs)


class OAuthRedirectParamError(OAuthParamError):
    def __init__(self, *args, **kwargs): # real signature unknown
        super(OAuthRedirectParamError, self).__init__(*args, **kwargs)


class FangcloudException(Exception):
    """All errors related to making an API request extend this."""

    def __init__(self, request_id, *args, **kwargs):
        # A request_id can be shared with Fangcloud Support to pinpoint the exact
        # request that returns an error.
        super(FangcloudException, self).__init__(request_id, *args, **kwargs)
        self.request_id = request_id

    def __str__(self):
        return repr(self)





