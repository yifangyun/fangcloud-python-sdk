import os
import unittest
import sys

from fangcloud.yifangyun import YfyClientFactory, YfyInit

access_token = os.environ.get('YFY_TOKEN')
if access_token is None:
    print('Set YFY_TOKEN environment variable to a valid token.')
    sys.exit(1)

access_refresh_token = os.environ.get('YFY_REFRESH_TOKEN')

client_id = os.environ.get('YFY_CLIENT_ID')
if client_id is None:
    print('Set YFY_CLIENT_ID environment is not variable.')
    sys.exit(1)

client_secret = os.environ.get('YFY_CLIENT_SECRET')
if client_secret is None:
    print('Set YFY_CLIENT_SECRET environment is not variable.')
    sys.exit(1)

YfyInit.init_system(client_id, client_secret)


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.yfy_client = YfyClientFactory.get_client_instance("user-id", access_token, access_refresh_token)

    def tearDown(self):
        pass


