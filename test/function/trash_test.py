import os

from .basic import BasicTest

trash_file = "trash_file.txt"


class TrashBasic(BasicTest):

    def setUp(self):
        super(TrashBasic, self).setUp()
        global trash_file
        self.new_file(trash_file)

    @staticmethod
    def new_file(name):
        with open(name, "w") as f:
            f.write(name)

    def tearDown(self):
        global trash_file
        if os.path.exists(trash_file):
            os.remove(trash_file)


class TrashFunctionTest(TrashBasic):

    def test_restore_all(self):
        result = self.yfy_client.file().upload_new_file(trash_file, 0)
        self.file_id = result["id"]
        self.yfy_client.file().delete_file(self.file_id)
        result = self.yfy_client.trash().restore_all()
        self.assertIsInstance(result, dict)
        self.yfy_client.file().delete_file(self.file_id)

    def test_clear(self):
        result = self.yfy_client.file().upload_new_file(trash_file, 0)
        self.file_id = result["id"]
        self.yfy_client.file().delete_file(self.file_id)
        result = self.yfy_client.trash().clear()
        self.assertIsInstance(result, dict)









