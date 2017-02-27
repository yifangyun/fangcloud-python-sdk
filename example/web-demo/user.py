
class User(object):

    __slots__ = [
        'username',
        'access_token',
        'refresh_token'
    ]

    def __init__(self, username, access_token, refresh_token):
        self.username = username
        self.access_token = access_token
        self.refresh_token = refresh_token

