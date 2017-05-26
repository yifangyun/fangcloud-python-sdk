import os

from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class FileRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FileRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def get_info(self, file_id):
        """
        获取文件信息
        :param file_id: 文件id
        :return: 文件信息
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.get_file_info(file_id)
        return self.get(url)

    def update_info(self, file_id, file_name, description=None):
        """
        更新文件信息

        :param file_id: 文件id
        :param file_name: 文件名
        :param description: 文件说明
        :return: 文件信息
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.update_file_info(file_id)
        pay_load = {
            "name": file_name,
            "description": None
        }
        return self.post(url, request_json_arg=pay_load)

    def get_upload_new_file_url(self, file_path, parent_id):
        """
        获取上传新文件的上传链接

        :param file_path: 文件上传的本地路径
        :param parent_id: 要上传的目标文件夹的id
        :return: 上传url
        """
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
        """
        上传新文件

        :param file_path: 文件上传的本地路径
        :param parent_id: 要上传的目标文件夹的id
        :return: 文件信息
        """
        upload_url = self.get_upload_new_file_url(file_path, parent_id)
        return self.post_file(upload_url, upload_file_path=file_path)

    def get_upload_new_version_url(self, file_id, file_path, remark=None):
        """
        获取上传新版本文件的上传链接

        :param file_id: 文件上传的本地路径
        :param file_path: 文件上传的本地路径
        :param remark: 上传新版本的备注
        :return: 上传url
        """
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
        """
        获取上传新版本

        :param file_id: 文件上传的本地路径
        :param file_path: 文件上传的本地路径
        :param remark: 上传新版本的备注
        :return: 文件信息
        """
        upload_url = self.get_upload_new_version_url(file_id, file_path, remark)
        return self.post_file(upload_url, upload_file_path=file_path)

    def download_file(self, file_id, file_path):
        """
        下载文件

        :param file_id: 文件id
        :param file_path: 文件上传的本地路径
        :return:
        """
        download_url = self.get_download_url(file_id)
        return self.get_file(download_url, file_path)

    def get_download_url(self, file_id):
        """
        获取下载文件的下载链接

        :param file_id:
        :return: 下载url
        """
        pre_sign_download_url = UrlBuilder.download_file(file_id)
        result = self.get(pre_sign_download_url)
        return result["download_urls"][str(file_id)]

    def delete_file(self, file_id):
        """
        删除文件

        :param file_id: 文件id
        :return: 删除结果
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.delete_file(file_id)
        return self.post(url)

    # def delete_file_batch(self, file_ids):
    #     """
    #     批量删除文件
    #
    #     :param file_ids: 文件列表
    #     :return:
    #     """
    #     assert isinstance(file_ids, list) or isinstance(file_ids, tuple)
    #     url = UrlBuilder.delete_file_batch()
    #     pay_load = {
    #         "file_ids": file_ids
    #     }
    #     return self.post(url, request_json_arg=pay_load)

    def restore_from_trash(self, file_id):
        """
        从回收站恢复文件

        :param file_id: 文件id
        :return:
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.restore_file_from_trash(file_id)
        return self.post(url)

    # def restore_from_trash_batch(self, file_ids):
    #     """
    #     批量从回收站恢复文件
    #
    #     :param file_ids: 文件id列表
    #     :return:
    #     """
    #     assert isinstance(file_ids, list) or isinstance(file_ids, tuple)
    #     url = UrlBuilder.restore_file_batch_from_trash()
    #     pay_load = {
    #         "file_ids": file_ids
    #     }
    #     return self.post(url, request_json_arg=pay_load)

    def delete_from_trash(self, file_id):
        """
        从回收站删除

        :param file_id: 文件id
        :return:
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.delete_file_from_trash(file_id)
        return self.post(url)

    def move_file(self, file_id, target_parent_id):
        """
        移动文件

        :param file_id: 文件id
        :param target_parent_id: 目标文件夹的id
        :return:
        """
        assert isinstance(file_id, int)
        assert isinstance(target_parent_id, int)
        url = UrlBuilder.move_file(file_id)
        pay_load = {
            "target_folder_id": target_parent_id
        }
        return self.post(url, request_json_arg=pay_load)

    def copy_file(self, file_id, target_folder_id, check_conflict=True):
        """
        拷贝文件

        :param file_id: 文件id
        :param target_folder_id: 目标文件夹的id
        :param check_conflict: 是否检查冲突, 如果检查冲突, 则云端有同名文件时, 会报错, 否则将文件自动重命名
        :return:
        """
        assert isinstance(file_id, int)
        assert isinstance(target_folder_id, int)
        assert isinstance(check_conflict, bool)
        url = UrlBuilder.copy_file(file_id)
        pay_load = {
            "target_folder_id": target_folder_id,
            "is_check_conflict": check_conflict
        }
        return self.post(url, request_json_arg=pay_load)

    def get_share_links(self, file_id, page_id=None, owner_id=None):
        """
        获取文件的所有分享链接, 其中page_id, owner_id为可选项

        :param file_id: 文件id
        :param page_id: 页码 (Optional)
        :param owner_id: 分享链接创建者id (Optional)
        :return: 分享链接
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.get_file_share_links(file_id)
        query = dict()
        if page_id is not None:
            query["page_id"] = page_id
        if owner_id is not None:
            query["owner_id"] = owner_id
        return self.get(url, params=query)

    def get_comments(self, file_id):
        """
        获取文件的评论列表

        :param file_id: 文件id
        :return: 文件评论列表
        """
        assert isinstance(file_id, int)
        url = UrlBuilder.get_file_comment(file_id)
        return self.get(url)


