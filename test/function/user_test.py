from function.basic import BasicTest


class UserTest(BasicTest):

    def test_get_user_info(self):
        result = self.yfy_client.user().get_self_info()
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIn("email", result)
        self.assertIn("active", result)
        self.assertIn("id", result)
        self.assertIn("pinyin_first_letters", result)
        self.assertIn("full_name_pinyin", result)
        self.assertIn("enterprise_id", result)
        self.assertIn("phone", result)



