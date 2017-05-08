from fangcloud.base_type import ItemType, SortBy, SortDirection
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class CommentRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(CommentRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def create_comment(self, file_id, content):
        assert isinstance(file_id, int)
        assert isinstance(content, str)
        url = UrlBuilder.create_comment()
        pay_load = {
            "file_id": file_id,
            "content": content
        }
        return self.post(url, request_json_arg=pay_load)

    def delete_comment(self, comment_id):
        url = UrlBuilder.delete_comment(comment_id)
        return self.post(url)




