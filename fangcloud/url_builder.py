import os


class UrlBuilder(object):

    _HOST = "https://platform.fangcloud.net"
    # _HOST = "https://platform-dev.fangcloud.net"

    @classmethod
    def set_host(cls, value):
        cls._HOST = value

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
    def delete_file(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/delete' % file_id])

    @classmethod
    def delete_file_batch(cls):
        return ''.join([cls._HOST, '/api', '/file/delete_batch'])

    @classmethod
    def restore_file_from_trash(cls):
        return ''.join([cls._HOST, '/api', '/file/restore_from_trash'])

    @classmethod
    def download_file(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/download' % file_id])

    @classmethod
    def move_file(cls, file_id):
        return ''.join([cls._HOST, '/api', '/file/%d/move' % file_id])

    @classmethod
    def copy_file(cls):
        return ''.join([cls._HOST, '/api', '/file/copy'])

    @classmethod
    def create_folder(cls):
        return ''.join([cls._HOST, '/api', '/folder/create'])

    @classmethod
    def delete_folder(cls, folder_id):
        return ''.join([cls._HOST, '/api', '/folder/%d/delete' % folder_id])

    @classmethod
    def get_folder_info(cls, folder_id):
        return ''.join([cls._HOST, '/api', '/folder/%d/info' % folder_id])

host = os.environ.get('YFY_HOST')
if host is not None:
    UrlBuilder.set_host(host)








