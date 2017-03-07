from function.basic import BasicTest

create_folder_name = 'unittest_folder'


class FolderBasic(BasicTest):

    def setUp(self):
        super(FolderBasic, self).setUp()
        # create new folder
        global create_folder_name
        result = self.yfy_client.folder().create_folder(create_folder_name, 0)
        self.check_folder_response(result)
        self.folder_id = result["id"]

    def check_folder_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("item_count", result)
        self.assertIn("description", result)
        self.assertIn("modified_at", result)
        self.assertIn("created_at", result)
        self.assertIn("folder_type", result)
        self.assertIn("sequence_id", result)
        self.assertIn("shared", result)
        self.assertIn("type", result)
        self.assertIn("size", result)
        self.assertIn("name", result)

        self.assertIn("path", result)
        self.assertIsInstance(result["path"], list)

        self.assertIn("parent", result)
        self.assertIn("id", result["parent"])
        self.assertIn("name", result["parent"])
        self.assertIn("type", result["parent"])

        self.assertIn("owned_by", result)
        self.assertIn("login", result["owned_by"])
        self.assertIn("name", result["owned_by"])
        self.assertIn("enterprise_id", result["owned_by"])
        self.assertIn("id", result["owned_by"])

    def tearDown(self):
        result = self.yfy_client.folder().delete_folder(self.folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)


class FolderFunctionTest(FolderBasic):

    def test_get_folder_info(self):
        pass


