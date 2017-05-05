from fangcloud.base_type import ItemType
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class FolderRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(FolderRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def create_folder(self, name, parent_id):
        """
        创建文件夹

        :param name: 文件夹名
        :param parent_id: 父文件夹id
        :return:
        """
        assert isinstance(name, str)
        assert isinstance(parent_id, int)
        url = UrlBuilder.create_folder()
        pay_load = {
            "name": name,
            "parent_id": parent_id
        }
        return self.post(url, request_json_arg=pay_load)

    def delete_folder(self, folder_id):
        """
        删除文件夹

        :param folder_id: 文件夹ID
        :return:
        """
        assert isinstance(folder_id, int)
        url = UrlBuilder.delete_folder(folder_id)
        return self.post(url)

    def restore_folder_from_trash(self, folder_id):
        """
        从回收站恢复文件夹

        :param folder_id: 文件夹ID
        :return:
        """
        assert isinstance(folder_id, int)
        url = UrlBuilder.restore_folder_from_trash(folder_id)
        return self.post(url)

    def delete_from_trash(self, folder_id):
        """
        从回收站删除文件夹

        :param folder_id: 文件夹ID
        :return:
        """
        assert isinstance(folder_id, int)
        url = UrlBuilder.delete_folder_from_trash(folder_id)
        return self.post(url)

    def get_folder_info(self, folder_id):
        """
        获取文件夹信息

        :param folder_id: 文件夹ID
        :return:
        """
        assert isinstance(folder_id, int)
        url = UrlBuilder.get_folder_info(folder_id)
        return self.get(url)

    def update_folder(self, folder_id, name):
        """
        更新文件夹

        :param folder_id: 文件夹ID
        :param name: 文件夹名
        :return:
        """
        assert isinstance(folder_id, int)
        assert isinstance(name, str)
        url = UrlBuilder.update_folder(folder_id)
        pay_load = {
            "name": name
        }
        return self.post(url, request_json_arg=pay_load)

    def move_folder(self, folder_id, target_parent_id):
        """
        移动文件夹

        :param folder_id: 文件夹ID
        :param target_parent_id: 目标父文件夹id
        :return:
        """
        assert isinstance(folder_id, int)
        assert isinstance(target_parent_id, int)
        url = UrlBuilder.move_folder(folder_id)
        pay_load = {
            "target_folder_id": target_parent_id
        }
        return self.post(url, request_json_arg=pay_load)

    def get_children(self, folder_id, page_id=0, page_capacity=20, item_type=ItemType.All):
        """
        获取单层子文件和文件夹列表

        :param folder_id:
        :param page_id: Default = 0
        :param page_capacity: Default = 20
        :param (optional) item_type: children item type, for example: file, folder, all. Default, all
        :return:
        """
        assert isinstance(folder_id, int)
        assert isinstance(page_id, int)
        assert isinstance(page_capacity, int)
        assert isinstance(item_type, str)
        url = UrlBuilder.get_children(folder_id)
        query = {
            "page_id": page_id,
            "page_capacity": page_capacity,
            "type": item_type
        }
        return self.get(url, params=query)

    def get_share_links(self, folder_id, page_id=None, owner_id=None):
        """
        获取文件夹的分享链接

        :param folder_id: 文件夹ID
        :param page_id: 页码 (Optional)
        :param owner_id: 分享链接创建者id (Optional)
        :return:
        """
        assert isinstance(folder_id, int)
        url = UrlBuilder.get_folder_share_links(folder_id)
        query = dict()
        if page_id is not None:
            query["page_id"] = page_id
        if owner_id is not None:
            query["owner_id"] = owner_id
        return self.get(url, params=query)

    def get_folder_collaborations(self, folder_id):
        """
        获取文件夹协作信息

        :param folder_id: 文件夹ID
        :return:
        """
        assert isinstance(folder_id, int)
        url = UrlBuilder.get_collaborations(folder_id)
        return self.get(url)

