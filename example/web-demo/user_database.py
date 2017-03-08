import json
import os
import threading
from json import JSONDecodeError

from user import User


def synchronized_method(method):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method


class UserDatabase(object):

    def __init__(self, file_path):
        self.user_database_file_path = file_path
        self.user_map = {}
        self.load_user_from_database()

    def load_user_from_database(self):
        user_list = []
        if os.path.exists(self.user_database_file_path):
            print("Loading User DB from file %s" % self.user_database_file_path)
            try:
                with open(self.user_database_file_path, "r") as user_file:
                    user_list = json.load(user_file)
            except JSONDecodeError:
                user_list = []
            print("Loaded %s records" % len(user_list))

        for user in user_list:
            self.user_map[user.get("name")] = User(user.get("name"), user.get("access_token"), user.get("refresh_token"))

    @synchronized_method
    def save_user_db(self):
        user_list = []
        for username in self.user_map.keys():
            user = self.user_map.get(username)
            user_json = {
                "name": user.username,
                "access_token": user.access_token,
                "refresh_token": user.refresh_token
            }
            user_list.append(user_json)
        with open(self.user_database_file_path, "w") as user_file:
            json.dump(user_list, user_file)

    def get_user(self, username):
        return self.user_map.get(username)

    def add_user(self, username, access_token = None, refresh_token = None):
        self.user_map[username] = User(username, access_token, refresh_token)

    def update_user(self, username, access_token, refresh_token):
        user = self.user_map.get(username)
        if user is not None:
            user.access_token = access_token
            user.refresh_token = refresh_token