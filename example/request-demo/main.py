
from config import Config
from fangcloud.yifangyun import YfyClientFactory


class FileHandler(object):

    def __init__(self, access_token):
        self.yfy_client = YfyClientFactory.get_client_instance("user-id", access_token)

    def get_file_info(self, file_id):
        return self.yfy_client.file().get_file_info(file_id)


if __name__ == '__main__':
    file_handler = FileHandler(Config.access_token)
    file_info = file_handler.get_file_info(501001367803)
    print(file_info)



