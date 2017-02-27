
class UrlBuilder(object):

    _HOST = "https://platform.fangcloud.net"

    @classmethod
    def get_file_info(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/info' % file_id])




