import os


class UrlBuilder(object):

    _HOST = "https://platform.fangcloud.net"
    _OAUTH_HOST = "https://oauth.fangcloud.net"
    _BASE_API = "/api/v2"
    # _HOST = "https://platform-dev.fangcloud.net"

    @classmethod
    def get_oauth_host(cls):
        return cls._OAUTH_HOST

    @classmethod
    def get_host(cls):
        return cls._HOST

    @classmethod
    def set_host(cls, value):
        cls._HOST = value

    @classmethod
    def get_file_info(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/info' % file_id])

    @classmethod
    def update_file_info(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/update' % file_id])

    @classmethod
    def upload_new_file_pre_sign(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/file/upload'])

    @classmethod
    def upload_new_version_pre_sign(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/new_version' % file_id])

    @classmethod
    def delete_file(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/delete' % file_id])

    @classmethod
    def delete_file_batch(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/file/delete_batch'])

    @classmethod
    def restore_file_from_trash(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/restore_from_trash' % file_id])

    @classmethod
    def restore_file_batch_from_trash(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/file/restore_from_trash'])

    @classmethod
    def delete_file_from_trash(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/delete_from_trash' % file_id])

    @classmethod
    def download_file(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/download' % file_id])

    @classmethod
    def move_file(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/move' % file_id])

    @classmethod
    def copy_file(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/copy' % file_id])

    @classmethod
    def get_file_share_links(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/share_links' % file_id])

    @classmethod
    def get_file_comment(cls, file_id):
        return ''.join([cls._HOST, cls._BASE_API, '/file/%d/comments' % file_id])

    @classmethod
    def create_folder(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/create'])

    @classmethod
    def delete_folder(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/delete' % folder_id])

    @classmethod
    def restore_folder_from_trash(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/restore_from_trash' % folder_id])

    @classmethod
    def delete_folder_from_trash(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/delete_from_trash' % folder_id])

    @classmethod
    def get_folder_info(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/info' % folder_id])

    @classmethod
    def update_folder(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/update' % folder_id])

    @classmethod
    def move_folder(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/move' % folder_id])

    @classmethod
    def get_folder_share_links(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/share_links' % folder_id])

    @classmethod
    def get_collaborations(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/collabs' % folder_id])

    @classmethod
    def get_children(cls, folder_id):
        return ''.join([cls._HOST, cls._BASE_API, '/folder/%d/children' % folder_id])

    @classmethod
    def search(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/item/search'])

    @classmethod
    def get_self_info(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/user/info'])

    @classmethod
    def clear_trash(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/trash/clear'])

    @classmethod
    def restore_trash(cls):
        return ''.join([cls._HOST, cls._BASE_API, '/trash/restore_all'])

host = os.environ.get('YFY_HOST')
if host is not None:
    UrlBuilder.set_host(host)








