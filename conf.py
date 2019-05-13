
import os


class Conf(dict):
    def __init__(self, store):
        super(Conf, self).__init__()
        if store is not None:
            self.update(store)

    def get(self, key, val=None):

        ret = os.environ.get(key) or (self[key] if key in self else val)

        if isinstance(ret, str):
            if ret.lower() == 'true':
                ret = True
            elif ret.lower() == 'false':
                ret = False

        return ret


config = {
    'LND_HOST': '127.0.0.1',
    'LND_PORT': 8080,
    'LND_CERT_PATH': '/home/nel0/.lnd/tls.cert',
    'LND_MACAROON_PATH': '/home/nel0/.lnd/data/chain/bitcoin/mainnet/admin.macaroon',

    'MYSQL_DB': 'lncity',
    'MYSQL_HOST': '127.0.0.1',
    'MYSQL_PORT': 3306,
    'MYSQL_USER': '',
    'MYSQL_PASS': '',

    'MAX_BALANCE_MOVEMENT': 500000,
    'MIN_BALANCE_MOVEMENT': 100,
    'INVOICE_TIMEOUT': 300,

    'VERSION': '0.0.1'
}

# Some configuration for my local test.
# I use the os name to identify that it is running on my laptop or in production
# My local machine is windows, the production server is ubuntu
if os.name == 'nt':
    config.update({
        'LND_HOST': '192.168.1.89',
        'LND_CERT_PATH': 'auth/tls.cert',
        'LND_MACAROON_PATH': 'auth/admin.macaroon',

        'MYSQL_USER': 'root',
        'MYSQL_PASS': 'OHzz%Xq%7dc6Sr5WX%gu'
    })

conf = Conf(config)
