import os

from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class FileRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FileRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def get_info(self, file_id):
        assert isinstance(file_id, int)
        url = UrlBuilder.get_file_info(file_id)
        return self.get(url)

    def update_info(self, file_id, file_name, description=None):
        assert isinstance(file_id, int)
        url = UrlBuilder.update_file_info(file_id)
        pay_load = {
            "name": file_name,
            "description": None
        }
        return self.post(url, request_json_arg=pay_load)

    def get_upload_new_file_url(self, file_path, parent_id):
        _, name = os.path.split(file_path)
        pre_sign_url = UrlBuilder.upload_new_file_pre_sign()
        pay_load = {
            "parent_id": parent_id,
            "name": name,
            "upload_type": "api"
        }
        result = self.post(pre_sign_url, request_json_arg=pay_load)
        return result["presign_url"]

    def upload_new_file(self, file_path, parent_id):
        upload_url = self.get_upload_new_file_url(file_path, parent_id)
        return self.post_file(upload_url, upload_file_path=file_path)

    def get_upload_new_version_url(self, file_id, file_path, remark=None):
        _, name = os.path.split(file_path)
        new_version_pre_sign_url = UrlBuilder.upload_new_version_pre_sign(file_id)
        pay_load = {
            "name": name,
            "upload_type": "api"
        }
        if remark is not None:
            pay_load["remark"] = remark
        result = self.post(new_version_pre_sign_url, request_json_arg=pay_load)
        return result["presign_url"]

    def upload_new_version(self, file_id, file_path, remark=None):
        upload_url = self.get_upload_new_version_url(file_id, file_path, remark)
        return self.post_file(upload_url, upload_file_path=file_path)

    def download_file(self, file_id, file_path):
        download_url = self.get_download_url(file_id)
        return self.get_file(download_url, file_path)

    def get_download_url(self, file_id):
        pre_sign_download_url = UrlBuilder.download_file(file_id)
        result = self.get(pre_sign_download_url)
        return result["download_urls"][str(file_id)]

    def delete_file(self, file_id):
        assert isinstance(file_id, int)
        url = UrlBuilder.delete_file(file_id)
        return self.post(url)

    def delete_file_batch(self, file_ids):
        assert isinstance(file_ids, list) or isinstance(file_ids, tuple)
        url = UrlBuilder.delete_file_batch()
        pay_load = {
            "file_ids": file_ids
        }
        return self.post(url, request_json_arg=pay_load)

    def restore_from_trash(self, file_id):
        assert isinstance(file_id, int)
        url = UrlBuilder.restore_file_from_trash(file_id)
        return self.post(url)

    def restore_from_trash_batch(self, file_ids):
        assert isinstance(file_ids, list) or isinstance(file_ids, tuple)
        url = UrlBuilder.restore_file_batch_from_trash()
        pay_load = {
            "file_ids": file_ids
        }
        return self.post(url, request_json_arg=pay_load)

    def delete_from_trash(self, file_id):
        assert isinstance(file_id, int)
        url = UrlBuilder.delete_file_from_trash(file_id)
        return self.post(url)

    def move_file(self, file_id, target_parent_id):
        assert isinstance(file_id, int)
        assert isinstance(target_parent_id, int)
        url = UrlBuilder.move_file(file_id)
        pay_load = {
            "target_folder_id": target_parent_id
        }
        return self.post(url, request_json_arg=pay_load)

    def copy_file(self, file_id, target_folder_id, check_conflict=True):
        assert isinstance(file_id, int)
        assert isinstance(target_folder_id, int)
        assert isinstance(check_conflict, bool)
        url = UrlBuilder.copy_file()
        pay_load = {
            "file_id": file_id,
            "target_folder_id": target_folder_id,
            "is_check_conflict": check_conflict
        }
        return self.post(url, request_json_arg=pay_load)






