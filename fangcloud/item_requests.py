from fangcloud.base_type import ItemType, SortBy, SortDirection
from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class ItemRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(ItemRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def search(self,
               query_words,
               item_type=ItemType.All,
               sort_by=SortBy.Name,
               sort_direction=SortDirection.Desc,
               page_number=0,
               search_in_folder=0):
        """
        :param (required) query_words: search key words
        :param (optional) item_type: search item type, for example: file, folder, all. Default, all
        :param (optional) sort_by: for example: name, date, size, score. Default: name
        :param (optional) sort_direction: for example: desc, asc. Default:
        :param (optional) page_number: Default: 0
        :param (optional) search_in_folder: 0
        :return:
        """
        assert isinstance(query_words, str)
        assert isinstance(item_type, str)
        assert isinstance(sort_by, str)
        assert isinstance(sort_direction, str)
        assert isinstance(page_number, int)
        assert isinstance(search_in_folder, int)
        url = UrlBuilder.search()
        query = {
            "query_words": query_words,
            "type": item_type,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "page_number": page_number,
            "search_in_folder": search_in_folder
        }
        return self.get(url, params=query)


