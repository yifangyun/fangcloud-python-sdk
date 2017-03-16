from fangcloud.base_type import ItemType, SortBy, SortDirection
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class TrashRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(TrashRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def clear(self, item_type=ItemType.All):
        url = UrlBuilder.clear_trash()
        query = {
            "type": item_type
        }
        return self.post(url, params=query)

    def restore_all(self, item_type=ItemType.All):
        url = UrlBuilder.restore_trash()
        query = {
            "type": item_type
        }
        return self.post(url, params=query)




