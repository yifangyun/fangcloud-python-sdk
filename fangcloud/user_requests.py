from fangcloud.transport import YfyTransport


class UserRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(UserRequests, self).__init__(self.client.access_token, self.client.refresh_token)