import threading

from abc import ABCMeta, abstractmethod

from fangcloud.folder_requests import FolderRequests
from fangcloud.item_requests import ItemRequests
from fangcloud.system_info import YfySystemInfo
from fangcloud.file_requests import FileRequests
from fangcloud.user_requests import UserRequests


class YfyNewTokenCallBack(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def on_token_refresh(self):
        """
        implement this function in subclass
        this function will be called when token refreshed
        """
        raise NotImplemented


class YfyClient(object):

    def __init__(self, access_token, refresh_token, call_back):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.call_back = call_back
        self._file_requests = FileRequests(self)
        self._folder_requests = FolderRequests(self)
        self._user_requests = UserRequests(self)
        self._item_requests = ItemRequests(self)

    def file(self):
        return self._file_requests

    def folder(self):
        return self._folder_requests

    def user(self):
        return self._user_requests

    def item(self):
        return self._item_requests


class YfyClientFactory(object):

    _clients = dict()
    _clients_lock = threading.Lock()

    @classmethod
    def get_client_instance(cls, key, access_token=None, refresh_token=None, call_back=None):
        assert key is not None and key != ""
        client = cls._clients.get(key, None)
        if client is None:
            with cls._clients_lock:
                # access_token is required to build YfyClient
                assert access_token is not None
                # call_back need to be subclass of YfyNewTokenCallBack and implement abstract function
                assert call_back is None or (call_back is not None and isinstance(call_back, YfyNewTokenCallBack))
                client = YfyClient(access_token, refresh_token, call_back)
                cls._clients[key] = client
        else:
            client.access_token = client.access_token if access_token is None else access_token
            client.refresh_token = client.refresh_token if refresh_token is None else refresh_token
            client.call_back = client.call_back if call_back is None else call_back
        return client


class YfyInit(object):

    @staticmethod
    def init_system(client_id, client_secret):
        YfySystemInfo.set_client(client_id, client_secret)














