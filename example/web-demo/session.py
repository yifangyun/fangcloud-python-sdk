import hashlib
import time


def md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()), encoding='utf-8'))
    return m.hexdigest()


class MemorySession:
    container = {}

    def __init__(self, handler):

        random_str = handler.get_cookie('yfy_session_id')
        if random_str:
            if random_str in MemorySession.container:
                self.r_str = random_str
            else:
                random_str = md5()
                MemorySession.container[random_str] = {}
                self.r_str = random_str
        else:
            random_str = md5()
            MemorySession.container[random_str] = {}
            self.r_str = random_str

        handler.set_cookie('yfy_session_id', random_str, expires=time.time() + 200)

    def __setitem__(self, key, value):
        MemorySession.container[self.r_str][key] = value

    def __getitem__(self, item):
        return MemorySession.container[self.r_str].get(item, None)

    def __delitem__(self, key):
        del MemorySession.container[self.r_str][key]