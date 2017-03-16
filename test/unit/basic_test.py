import unittest

import requests

from fangcloud.session import create_session


class BasicTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_session(self):
        result = create_session(max_connections=10)
        self.assertIsInstance(result, requests.Session)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()






