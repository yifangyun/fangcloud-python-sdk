
class YfySystemInfo:

    client_id = None
    client_secret = None

    sdk_version = "0.0.1"

    @classmethod
    def set_client(cls, client_id, client_secret):
        cls.client_id = client_id
        cls.client_secret = client_secret

    @classmethod
    def get_client_id(cls):
        return cls.client_id

    @classmethod
    def get_client_secret(cls):
        return cls.client_secret



