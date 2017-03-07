from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class FolderRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FolderRequests, self).__init__(self.client.access_token, self.client.refresh_token)

    def create_folder(self, name, parent_id):
        assert isinstance(name, str)
        assert isinstance(parent_id, int)
        url = UrlBuilder.create_folder()
        pay_load = {
            "name": name,
            "parent_id": parent_id
        }
        return self.post(url, request_json_arg=pay_load)

    def delete_folder(self, folder_id):
        assert isinstance(folder_id, int)
        url = UrlBuilder.delete_folder(folder_id)
        return self.post(url)




