import os

from .basic import BasicTest

download_file_path = "unittest_download_file"
rename_file_path = "renamed_by_unittest"
folder_name = "unittest_folder_for_file"
upload_file_txt = "test_upload.txt"
delete_from_trash_file_txt = "delete_from_trash_file.txt"


class FileBasic(BasicTest):
    """
    File basic test includes file upload and delete
    """
    def setUp(self):
        super(FileBasic, self).setUp()
        # upload single file
        self.new_file(upload_file_txt)
        self.new_file(delete_from_trash_file_txt)
        result = self.yfy_client.file().upload_new_file(upload_file_txt, 0)
        self.check_file_response(result)
        self.file_id = result["id"]
        result = self.yfy_client.folder().create_folder(folder_name, 0)
        self.folder_id = result["id"]

    @staticmethod
    def new_file(name):
        with open(name, "w") as f:
            f.write(name)

    def check_file_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("type", result)
        self.assertIn("description", result)
        self.assertIn("sha1", result)
        self.assertIn("sequence_id", result)
        self.assertIn("comments_count", result)
        self.assertIn("created_at", result)

        self.assertIn("parent", result)
        self.assertIn("type", result["parent"])
        self.assertIn("name", result["parent"])
        self.assertIn("id", result["parent"])

        self.assertIn("size", result)
        self.assertIn("name", result)
        self.assertIn("path", result)
        self.assertIsInstance(result["path"], list)
        self.assertIn("modified_at", result)
        self.assertIn("owned_by", result)

        self.assertIn("name", result["owned_by"])
        self.assertIn("enterprise_id", result["owned_by"])
        self.assertIn("login", result["owned_by"])
        self.assertIn("id", result["owned_by"])

    def check_url(self, url):
        self.assertIsInstance(url, str)
        self.assertEqual(url.startswith("http"), True)  # url starts with http or https

    def tearDown(self):
        global download_file_path
        result = self.yfy_client.file().delete_file(self.file_id)
        self.assertIsInstance(result, dict)
        if os.path.exists(download_file_path):
            os.remove(download_file_path)
        result = self.yfy_client.folder().delete_folder(self.folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        if os.path.exists(delete_from_trash_file_txt):
            os.remove(delete_from_trash_file_txt)
        if os.path.exists(upload_file_txt):
            os.remove(upload_file_txt)

class FileFunctionTest(FileBasic):

    def test_get_file_info(self):
        result = self.yfy_client.file().get_info(self.file_id)
        self.check_file_response(result)

    def test_update_file_info(self):
        global rename_file_path
        result = self.yfy_client.file().update_info(self.file_id, rename_file_path)
        self.check_file_response(result)

    def test_get_upload_url(self):
        result = self.yfy_client.file().get_upload_new_file_url(upload_file_txt, 0)
        self.check_url(result)

    def test_get_upload_new_version_url(self):
        result = self.yfy_client.file().get_upload_new_version_url(self.file_id, upload_file_txt)
        self.check_url(result)

    def test_upload_new_version(self):
        result = self.yfy_client.file().upload_new_version(self.file_id, upload_file_txt, remark="upload new version")
        self.assertIsInstance(result, dict)
        self.check_file_response(result)

    def test_download_file(self):
        global download_file_path
        result = self.yfy_client.file().download_file(self.file_id, download_file_path)
        self.assertEqual(result, True)
        self.assertEqual(os.path.exists(download_file_path), True)

    def test_get_download_url(self):
        result = self.yfy_client.file().get_download_url(self.file_id)
        self.check_url(result)

    def test_move_file(self):
        result = self.yfy_client.file().move_file(self.file_id, self.folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        # move back
        result = self.yfy_client.file().move_file(self.file_id, 0)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)

    def test_copy_file(self):
        result = self.yfy_client.file().copy_file(self.file_id, self.folder_id, True)
        self.check_file_response(result)

    def test_restore_file_from_trash(self):
        result = self.yfy_client.file().delete_file(self.file_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["success"], True)
        result = self.yfy_client.file().restore_from_trash(self.file_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)

    def test_delete_from_trash(self):
        result = self.yfy_client.file().upload_new_file(delete_from_trash_file_txt, 0)
        self.check_file_response(result)
        file_id = result["id"]
        result = self.yfy_client.file().delete_file(file_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["success"], True)
        result = self.yfy_client.file().delete_from_trash(file_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["success"], True)

    def test_get_file_share_links(self):
        result = self.yfy_client.file().get_share_links(self.file_id)
        self.assertIsInstance(result, dict)
        self.assertIn("total_count", result)
        self.assertIn("page_id", result)
        self.assertIn("page_count", result)
        self.assertIn("share_links", result)

    def test_get_file_comment(self):
        result = self.yfy_client.file().get_comments(self.file_id)
        self.assertIsInstance(result, dict)
        self.assertIn("comments", result)
        self.assertIsInstance(result["comments"], list)





