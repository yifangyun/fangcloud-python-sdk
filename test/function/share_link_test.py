import os

from fangcloud.base_type import ShareLinkAccess
from .basic import BasicTest

comment_file = "trash_file.txt"

share_link_file_test = "share_link_file_test.txt"
share_link_folder_test = "share_link_folder_test"


class ShareLinkBasic(BasicTest):

    def setUp(self):
        super(ShareLinkBasic, self).setUp()
        # upload single file
        self.new_file(share_link_file_test)
        result = self.yfy_client.file().upload_new_file(share_link_file_test, 0)
        self.file_id = result["id"]
        result = self.yfy_client.folder().create_folder(share_link_folder_test, 0)
        self.folder_id = result["id"]

        result = self.yfy_client.share_link().create_file_share_link(self.file_id, ShareLinkAccess.Public, "2018-03-20")
        self.check_share_link_response(result)

        result = self.yfy_client.share_link().create_folder_share_link(self.folder_id, ShareLinkAccess.Public, "2018-03-20")
        self.check_share_link_response(result)
        self.unique_name = result["unique_name"]

    @staticmethod
    def new_file(name):
        with open(name, "w") as f:
            f.write(name)

    def check_share_link_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn("unique_name", result)
        self.assertIn("share_link", result)
        self.assertIn("access", result)
        self.assertIn("password_protected", result)
        self.assertIn("due_time", result)
        self.assertIn("disable_download", result)

    def tearDown(self):
        global share_link_file_test
        result = self.yfy_client.file().delete_file(self.file_id)
        self.assertIsInstance(result, dict)
        if os.path.exists(share_link_file_test):
            os.remove(share_link_file_test)
        result = self.yfy_client.folder().delete_folder(self.folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)


class ShareLinkFunctionTest(ShareLinkBasic):

    def test_get_share_link_info(self):
        result = self.yfy_client.share_link().get_share_link_info(self.unique_name)
        self.check_share_link_response(result)

    def test_update_share_link_info(self):
        result = self.yfy_client.share_link().update_share_link_info(self.unique_name, ShareLinkAccess.Public, "2018-03-21")
        self.check_share_link_response(result)

    def test_delete_share_link(self):
        result = self.yfy_client.share_link().delete_share_link(self.unique_name)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)










