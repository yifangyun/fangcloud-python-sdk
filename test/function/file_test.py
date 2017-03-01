

from .basic import BasicTest


class FileFunctionTest(BasicTest):

    def test_get_file_info(self):
        result = self.yfy_client.file().get_info(501001367803)
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("owned_by", result)
        self.assertIn("created_at", result)
        self.assertIn("comments_count", result)
        self.assertIn("in_trash", result)
        self.assertIn("type", result)
        self.assertIn("path", result)
        self.assertIn("sequence_id", result)
        self.assertIn("modified_at", result)
        self.assertIn("is_deleted", result)
        self.assertIn("extension_category", result)
        self.assertIn("name", result)
        self.assertIn("size", result)
        self.assertIn("description", result)
        self.assertIn("parent", result)

    def test_update_file_info(self):
        result = self.yfy_client.file().update_info(501001367803, "renamed_by_test")
        self.assertIsInstance(result, dict)

    def test_upload_file(self):
        result = self.yfy_client.file().upload_new_file("basic.py", 0)
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)

    def test_download_file(self):
        pass




