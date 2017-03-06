
from .basic import BasicTest


class FileBasic(BasicTest):
    """
    File basic test includes file upload and delete
    """
    def setUp(self):
        super(FileBasic, self).setUp()
        # upload single file
        result = self.yfy_client.file().upload_new_file("__init__.py", 0)
        self.check_file_response(result)
        self.file_id = result["id"]

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

    def tearDown(self):
        result = self.yfy_client.file().delete_file(self.file_id)
        self.assertIsInstance(result, dict)


class FileFunctionTest(FileBasic):

    def test_get_file_info(self):
        result = self.yfy_client.file().get_info(self.file_id)
        self.check_file_response(result)

    def test_update_file_info(self):
        result = self.yfy_client.file().update_info(self.file_id, "renamed_by_test1")
        self.check_file_response(result)

    def test_download_file(self):
        pass




