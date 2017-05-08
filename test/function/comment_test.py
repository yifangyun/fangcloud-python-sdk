import os

from .basic import BasicTest

comment_file = "comment_file.txt"


class CommentBasic(BasicTest):

    def setUp(self):
        super(CommentBasic, self).setUp()
        global comment_file
        self.new_file(comment_file)
        result = self.yfy_client.file().upload_new_file(comment_file, 0)
        self.file_id = result["id"]

        #create comment
        result = self.yfy_client.comment().create_comment(self.file_id, "this is test comment from python sdk")
        self.assertIsInstance(result, dict)
        self.assertIn("comment_id", result)
        self.assertIn("content", result)
        self.assertIn("created_at", result)
        self.assertIn("file_id", result)
        self.assertIn("user", result)
        self.comment_id = result["comment_id"]

    @staticmethod
    def new_file(name):
        with open(name, "w") as f:
            f.write(name)

    def tearDown(self):
        global comment_file
        self.yfy_client.file().delete_file(self.file_id)
        if os.path.exists(comment_file):
            os.remove(comment_file)


class CommentFunctionTest(CommentBasic):

    def test_delete_comment(self):
        result = self.yfy_client.comment().delete_comment(self.comment_id)
        self.assertIn("success", result)









