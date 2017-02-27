
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class FileRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FileRequests, self).__init__(self.client.access_token, self.client.refresh_token)

    def get_file_info(self, file_id):
        url = UrlBuilder.get_file_info(file_id)
        return self.get(url)


class FolderRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FolderRequests, self).__init__(self.client.access_token, self.client.refresh_token)


class UserRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(UserRequests, self).__init__(self.client.access_token, self.client.refresh_token)


