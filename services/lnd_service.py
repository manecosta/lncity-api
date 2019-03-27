
import codecs
import requests
import json

from conf import conf


class LNDService:

    def __init__(self, host: str = None, port: int = None, cert_path: str = None, macaroon_path: str = None):
        self._host = host or conf.get('LND_HOST')
        self._port = port or conf.get('LND_PORT')
        self._cert_path = cert_path or conf.get('LND_CERT_PATH')
        self._macaroon_path = macaroon_path or conf.get('LND_MACAROON_PATH')

        self._encoded_macaroon = codecs.encode(open(conf.get('LND_MACAROON_PATH'), 'rb').read(), 'hex')

        self._base_url = f'https://{self._host}:{self._port}/v1'

    @property
    def _headers(self):
        return {'Grpc-Metadata-macaroon': self._encoded_macaroon}

    def _post(self, endpoint, **kwargs):
        if not endpoint:
            return None
        elif endpoint[0] != '/':
            endpoint = f'/{endpoint}'

        response = requests.post(
            f'{self._base_url}{endpoint}',
            headers=self._headers,
            verify=self._cert_path,
            data=json.dumps(kwargs)
        )

        response.raise_for_status()

        return response.json()

    def _get(self, endpoint, *args):
        if not endpoint:
            return None
        elif endpoint[0] != '/':
            endpoint = f'/{endpoint}'

        if not endpoint:
            return None
        elif endpoint[0] != '/':
            endpoint = f'/{endpoint}'

        response = requests.post(
            f'{self._base_url}{endpoint}/{"/".join(args)}',
            headers=self._headers,
            verify=self._cert_path
        )

        response.raise_for_status()

        return response.json()

    def invoices_new(self, amount: float, memo: str = None):
        try:
            invoice = self._post('/invoices', amount=amount, memo=memo)
        except Exception:
            return None

        return invoice
