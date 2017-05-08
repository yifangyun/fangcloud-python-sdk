from fangcloud.base_type import ItemType, SortBy, SortDirection, CollaborationRole
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class CollaborationRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(CollaborationRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    @staticmethod
    def _check_role(role):
        assert role in [CollaborationRole.Coowner,
                        CollaborationRole.Edit,
                        CollaborationRole.Owner,
                        CollaborationRole.Previewer,
                        CollaborationRole.Uploader,
                        CollaborationRole.Viewer,
                        CollaborationRole.ViewerUploader
                        ]

    def invite_collaborator(self, folder_id, user_id, role, message=None):
        """
        邀请协作

        :param folder_id: 文件夹id
        :param user_id: 用户id
        :param role: 协作角色, 必须为CollaborationRole中的一种
        :param message: 协作信息,可以选
        :return:
        """
        assert isinstance(folder_id, int)
        assert isinstance(user_id, int)
        self._check_role(role)
        url = UrlBuilder.collaboration_invite()
        invited_user = {
            "id": user_id,
            "role": role
        }
        pay_load = {
            "folder_id": folder_id,
            "invited_user": invited_user
        }
        if message is not None:
            pay_load["invitation_message"] = message
        return self.post(url, request_json_arg=pay_load)

    def get_collaboration(self, collaboration_id):
        assert isinstance(collaboration_id, int)
        url = UrlBuilder.get_collaboration_info(collaboration_id)
        return self.get(url)

    def update_collaboration(self, collaboration_id, role):
        assert isinstance(collaboration_id, int)
        self._check_role(role)
        url = UrlBuilder.update_collaboration(collaboration_id)
        pay_load = {
            "role": role
        }
        return self.post(url, request_json_arg=pay_load)

    def delete_collaboration(self, collaboration_id):
        assert isinstance(collaboration_id, int)
        url = UrlBuilder.delete_collaboration(collaboration_id)
        return self.post(url)






