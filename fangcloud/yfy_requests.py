import os

from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class FileRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FileRequests, self).__init__(self.client.access_token, self.client.refresh_token)

    def get_info(self, file_id):
        assert isinstance(file_id, int)
        url = UrlBuilder.get_file_info(file_id)
        return self.get(url)

    def update_info(self, file_id, file_name):
        assert isinstance(file_id, int)
        url = UrlBuilder.update_file_info(file_id)
        pay_load = {
            "name": file_name
        }
        return self.put(url, request_json_arg=pay_load)

    def upload_new_file(self, file_path, parent_id):
        _, name = os.path.split(file_path)
        pre_sign_url = UrlBuilder.upload_new_file_pre_sign()
        pay_load = {
            "parent_id": parent_id,
            "name": name,
            "upload_type": "api"
        }
        result = self.post(pre_sign_url, request_json_arg=pay_load)
        upload_url = result["presign_url"]
        return self.post_file(upload_url, upload_file_path=file_path)

    def download_file(self, file_id, file_path):
        pre_sign_download_url = UrlBuilder.download_file(file_id)
        result = self.get(pre_sign_download_url)
        download_url = result["download_urls"][str(file_id)]

    def delete_files(self, file_ids):
        assert isinstance(file_ids, list) or isinstance(file_ids, tuple)
        url = UrlBuilder.delete_file()
        pay_load = {
            "file_ids": file_ids
        }
        return self.delete(url, request_json_arg=pay_load)

    def restore_from_trash(self, file_ids):
        assert isinstance(file_ids, list) or isinstance(file_ids, tuple)
        url = UrlBuilder.restore_file_from_trash()
        pay_load = {
            "file_ids": file_ids
        }
        return self.post(url, request_json_arg=pay_load)


class FolderRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FolderRequests, self).__init__(self.client.access_token, self.client.refresh_token)


class UserRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(UserRequests, self).__init__(self.client.access_token, self.client.refresh_token)


