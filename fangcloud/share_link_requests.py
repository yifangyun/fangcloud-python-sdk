from fangcloud.base_type import ItemType, SortBy, SortDirection, ShareLinkAccess
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class ShareLinkRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(ShareLinkRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def create_item_share_link(self, type, item_id, access, due_time, disable_download=None, password_protected=None, password=None):
        """
        创建分享链接

        :param (int) item_id: 文件或者文件夹的id
        :param (string) access: 权限范围, 必须为ShareLinkAccess.Public 或者ShareLinkAccess.Company
        :param (string) due_time: 到期时间, 格式必须为: "2017-03-20"
        :param (boolean) disable_download: 是否不允许下载(默认false)
        :param (boolean) password_protected: 是否有密码(默认false)
        :param (string) password: 密码
        :return: 分享链接信息, 例如:

                {
                  "unique_name": "asfsdgdrftyhgfjhgj",
                  "share_link": "https://www.fangcloud.net/share/asfsdgdrftyhgfjhgj",
                  "access": "public",
                  "password_protected": false,
                  "due_time": "2017-03-20",
                  "disable_download": false
                }

        """
        assert isinstance(item_id, int)
        assert access in [ShareLinkAccess.Public, ShareLinkAccess.Company]
        url = UrlBuilder.create_share_link()
        pay_load = {
            "access": access,
            "due_time": due_time
        }
        if type == "file":
            pay_load["file_id"] = item_id
        elif type == "folder":
            pay_load["folder_id"] = item_id
        else:
            raise AssertionError

        if disable_download is not None:
            assert isinstance(disable_download, bool)
            pay_load["disable_download"] = disable_download
        if password_protected is not None and password is not None:
            assert isinstance(password_protected, bool)
            assert isinstance(password, str)
            pay_load["password_protected"] = password_protected
            pay_load["password"] = password
        return self.post(url, request_json_arg=pay_load)

    def create_folder_share_link(self, folder_id, access, due_time, disable_download=None, password_protected=None, password=None):
        return self.create_item_share_link("folder", folder_id, access, due_time, disable_download, password_protected, password)

    def create_file_share_link(self, file_id, access, due_time, disable_download=None, password_protected=None, password=None):
        return self.create_item_share_link("file", file_id, access, due_time, disable_download, password_protected, password)

    def get_share_link_info(self, unique_name):
        """
        获取分享链接的信息

        :param unique_name: 分享链接标识符
        :return:
        """
        assert isinstance(unique_name, str)
        url = UrlBuilder.get_share_link_info(unique_name)
        return self.get(url)

    def update_share_link_info(self, unique_name, access, due_time, disable_download=None, password_protected=None, password=None):
        assert isinstance(unique_name, str)
        assert access in [ShareLinkAccess.Public, ShareLinkAccess.Company]
        url = UrlBuilder.update_share_link_info(unique_name)
        pay_load = {
            "access": access,
            "due_time": due_time
        }
        if disable_download is not None:
            assert isinstance(disable_download, bool)
            pay_load["disable_download"] = disable_download
        if password_protected is not None and password is not None:
            assert isinstance(password_protected, bool)
            assert isinstance(password, str)
            pay_load["password_protected"] = password_protected
            pay_load["password"] = password
        return self.post(url, request_json_arg=pay_load)

    def delete_share_link(self, unique_name):
        assert isinstance(unique_name, str)
        url = UrlBuilder.revoke_share_link(unique_name)
        return self.post(url)







