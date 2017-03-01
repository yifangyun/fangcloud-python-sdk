import os
import unittest
import sys

from fangcloud.yifangyun import YfyClientFactory

access_token = os.environ.get('YFY_TOKEN')
if access_token is None:
    print('Set YFY_TOKEN environment variable to a valid token.')
    sys.exit(1)


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.yfy_client = YfyClientFactory.get_client_instance("user-id", access_token)

    def tearDown(self):
        pass


