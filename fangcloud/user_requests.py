from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class UserRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(UserRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def get_self_info(self):
        url = UrlBuilder.get_self_info()
        return self.get(url)



