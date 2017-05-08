import os

from fangcloud.base_type import CollaborationRole
from .basic import BasicTest

collaboration_folder_name = "collaboration_folder"


class CollaborationBasic(BasicTest):

    def setUp(self):
        super(CollaborationBasic, self).setUp()
        global collaboration_folder_name
        result = self.yfy_client.folder().create_folder(collaboration_folder_name, 0)
        self.folder_id = result["id"]
        result = self.yfy_client.collaboration().invite_collaborator(self.folder_id, 1, CollaborationRole.Coowner)
        self.check_collaboration(result)
        self.collaboration_id = result["collab_id"]

    def check_collaboration(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn("collab_id", result)
        self.assertIn("user", result)
        self.assertIn("accepted", result)
        self.assertIn("role", result)

    def tearDown(self):
        result = self.yfy_client.folder().delete_folder(self.folder_id)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)


class CollaborationFunctionTest(CollaborationBasic):

    def test_get_collaboration(self):
        result = self.yfy_client.collaboration().get_collaboration(self.collaboration_id)
        self.check_collaboration(result)

    def test_update_collaboration(self):
        result = self.yfy_client.collaboration().update_collaboration(self.collaboration_id, CollaborationRole.Viewer)
        self.check_collaboration(result)

    def test_delete_collaboration(self):
        result = self.yfy_client.collaboration().delete_collaboration(self.collaboration_id)
        self.assertIn("success", result)






