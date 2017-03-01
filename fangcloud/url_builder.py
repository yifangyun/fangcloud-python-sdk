
class UrlBuilder(object):

    _HOST = "https://platform.fangcloud.net"

    @classmethod
    def get_file_info(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/info' % file_id])

    @classmethod
    def update_file_info(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/update' % file_id])

    @classmethod
    def upload_new_file_pre_sign(cls):
        return ''.join([cls._HOST, '/api', '/file/upload'])

    @classmethod
    def delete_file(cls):
        return ''.join([cls._HOST, '/api', '/file/delete'])

    @classmethod
    def restore_file_from_trash(cls):
        return ''.join([cls._HOST, '/api', '/file/restore_from_trash'])

    @classmethod
    def download_file(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/download' % file_id])











