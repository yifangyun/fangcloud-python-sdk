from function.basic import BasicTest

create_folder_name = 'unittest_folder'
rename_folder = 'rename_folder'
move_folder_parent_folder = 'move_folder_parent_folder'


class FolderBasic(BasicTest):

    def setUp(self):
        super(FolderBasic, self).setUp()
        # create new folder
        global create_folder_name
        result = self.yfy_client.folder().create_folder(create_folder_name, 0)
        self.check_folder_response(result)
        self.folder_id = result["id"]
        result = self.yfy_client.folder().create_folder(move_folder_parent_folder, 0)
        self.check_folder_response(result)
        self.parent_folder_id = result["id"]

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
        result = self.yfy_client.folder().delete_folder(self.parent_folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)


class FolderFunctionTest(FolderBasic):

    def test_get_folder_info(self):
        result = self.yfy_client.folder().get_folder_info(self.folder_id)
        self.check_folder_response(result)

    def test_update_folder(self):
        result = self.yfy_client.folder().update_folder(self.folder_id, "rename_folder")
        self.check_folder_response(result)

    def test_move_folder(self):
        result = self.yfy_client.folder().move_folder(self.folder_id, self.parent_folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)

    def test_search(self):
        result = self.yfy_client.item().search(create_folder_name)
        self.assertIsInstance(result, dict)
        self.assertIn("page_id", result)
        self.assertIn("page_capacity", result)
        self.assertIn("files", result)
        self.assertIn("folders", result)
        self.assertIn("total_count", result)




