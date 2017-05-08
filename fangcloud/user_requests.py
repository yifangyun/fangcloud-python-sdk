from fangcloud.transport import YfyTransport
from fangcloud.url_builder import UrlBuilder


class UserRequests(YfyTransport):

    def __init__(self, client):
        self.client = client
        super(UserRequests, self).__init__(self.client.access_token, self.client.refresh_token, self.client.call_back)

    def get_self_info(self):
        url = UrlBuilder.get_self_info()
        return self.get(url)

    def get_user_info(self, user_id):
        url = UrlBuilder.get_user_info(user_id)
        return self.get(url)

    def get_user_profile_pic_file(self, user_id, profile_pic_key, file_path):
        url = UrlBuilder.get_user_pic(user_id)
        query = {
            "profile_pic_key": profile_pic_key
        }
        self.get_file(url, file_path, params=query)

    def update_user_info(self, name):
        assert isinstance(name, str)
        url = UrlBuilder.update_user_info()
        pay_load = {
            "name": name
        }
        return self.post(url, request_json_arg=pay_load)

    def get_user_space(self):
        url = UrlBuilder.get_space_usage()
        return self.get(url)

    def search_user(self, query_words, page_id):
        """
        本企业内的用户搜索

        :param query_words: 搜索关键字
        :param page_id: 页码
        :return: 用户列表
        """
        assert isinstance(query_words, str)
        assert isinstance(page_id, int)
        url = UrlBuilder.search_user()
        query = {
            "query_words": query_words,
            "page_id": page_id
        }
        return self.get(url, params=query)





