import os

from .basic import BasicTest

profile_pic_file = "profile_pic_file"


class UserBasicTest(BasicTest):

    def setUp(self):
        super(UserBasicTest, self).setUp()
        result = self.yfy_client.user().get_self_info()
        self.check_user_response(result)
        self.user_id = result["id"]
        self.profile_pic_key = result["profile_pic_key"]

    def check_user_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIn("email", result)
        self.assertIn("active", result)
        self.assertIn("id", result)
        self.assertIn("pinyin_first_letters", result)
        self.assertIn("full_name_pinyin", result)
        self.assertIn("enterprise", result)
        self.assertIn("id", result["enterprise"])
        self.assertIn("name", result["enterprise"])
        self.assertIn("admin_user_id", result["enterprise"])
        self.assertIn("phone", result)
        self.assertIn("profile_pic_key", result)

    def tearDown(self):
        global profile_pic_file
        if os.path.exists(profile_pic_file):
            os.remove(profile_pic_file)


class UserTest(UserBasicTest):

    def test_get_user_info(self):
        result = self.yfy_client.user().get_user_info(self.user_id)
        self.check_user_response(result)

    def test_get_user_profile_pic(self):
        self.yfy_client.user().get_user_profile_pic_file(self.user_id, self.profile_pic_key, profile_pic_file)

    def test_update_user_info(self):
        result = self.yfy_client.user().update_user_info("tt")
        self.check_user_response(result)

    def test_user_space(self):
        result = self.yfy_client.user().get_user_space()
        self.assertIsInstance(result, dict)
        self.assertIn("space_used", result)
        self.assertIn("space_total", result)

    def test_search_user(self):
        result = self.yfy_client.user().search_user("asdf", 0)
        self.assertIsInstance(result, dict)
        self.assertIn("users", result)









