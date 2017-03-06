
from config import Config
from fangcloud.yifangyun import YfyClientFactory, YfyInit

YfyInit.init_yifangyun(Config.client_id, Config.client_secret)


class FileHandler(object):

    def __init__(self, access_token):
        self.yfy_client = YfyClientFactory.get_client_instance("user-id", access_token)

    def get_file_info(self, file_id):
        return self.yfy_client.file().get_info(file_id)

    def update_file_info(self, file_id, file_name):
        return self.yfy_client.file().update_info(file_id, file_name)

    def upload_file(self, file_path):
        return self.yfy_client.file().upload_new_file(file_path, 0)

if __name__ == '__main__':
    file_handler = FileHandler(Config.access_token)
    file_handler.update_file_info(501001367803, "renamed_by_test")

    # file_info = file_handler.get_file_info(501001367803)
    # print(file_info)
    # file_info = file_handler.upload_file("/Users/lrenjundk/Documents/workspace-python/python-sdk/example/request-demo/config.py")
    # print(file_info)


