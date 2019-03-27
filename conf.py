
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


conf = Conf({
    # 'LND_HOST': '127.0.0.1',
    'LND_PORT': '8080',
    # 'LND_CERT_PATH': '/home/nel0/.lnd/tls.cert',
    # 'LND_MACAROON_PATH': '/home/nel0/.lnd/data/chain/bitcoin/mainnet/admin.macaroon'

    'LND_HOST': '192.168.1.89',
    'LND_CERT_PATH': 'auth/tls.cert',
    'LND_MACAROON_PATH': 'auth/admin.macaroon'
})
