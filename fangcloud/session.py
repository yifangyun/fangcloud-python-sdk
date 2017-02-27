import ssl
import pkg_resources
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

_TRUSTED_CERT_FILE = pkg_resources.resource_filename(__name__, 'trusted-certs.crt')


class _SSLAdapter(HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       cert_reqs=ssl.CERT_REQUIRED,
                                       ca_certs=_TRUSTED_CERT_FILE,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def pinned_session(pool_maxsize=8):
    http_adapter = _SSLAdapter(pool_connections=4,
                               pool_maxsize=pool_maxsize)

    _session = requests.session()
    _session.mount('https://', http_adapter)

    return _session


def create_session(max_connections=8, proxies=None):
    session = pinned_session(pool_maxsize=max_connections)
    if proxies:
        session.proxies = proxies
    return session
