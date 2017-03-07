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

    def get_folder_info(self, folder_id):
        assert isinstance(folder_id, int)
        url = UrlBuilder.get_folder_info(folder_id)
        return self.get(url)

    def update_folder(self, folder_id, name):
        assert isinstance(folder_id, int)
        assert isinstance(name, str)
        url = UrlBuilder.update_folder(folder_id)
        pay_load = {
            "name": name
        }
        return self.post(url, request_json_arg=pay_load)

    def move_folder(self, folder_id, target_parent_id):
        assert isinstance(folder_id, int)
        assert isinstance(target_parent_id, int)
        url = UrlBuilder.move_folder(folder_id)
        pay_load = {
            "target_folder_id": target_parent_id
        }
        return self.post(url, request_json_arg=pay_load)





