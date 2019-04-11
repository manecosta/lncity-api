
import codecs
from typing import Optional, List, Union

import requests
import json
import logging
import urllib.parse
import base64

from conf import conf

logging.basicConfig(level=logging.DEBUG)


class LND:

    def __init__(self, host: str = None, port: int = None, cert_path: str = None, macaroon_path: str = None):
        self._host = host or conf.get('LND_HOST')
        self._port = port or conf.get('LND_PORT')
        self._cert_path = cert_path or conf.get('LND_CERT_PATH')
        self._macaroon_path = macaroon_path or conf.get('LND_MACAROON_PATH')

        self._encoded_macaroon = codecs.encode(open(conf.get('LND_MACAROON_PATH'), 'rb').read(), 'hex')

        self._base_url = f'https://{self._host}:{self._port}/v1'

    @property
    def _headers(self) -> dict:
        return {'Grpc-Metadata-macaroon': self._encoded_macaroon}

    def _post(self, endpoint, **kwargs) -> Optional[Union[list, dict]]:
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

    def _get(self, endpoint, **kwargs) -> Optional[Union[dict, list]]:
        if not endpoint:
            return None
        elif endpoint[0] != '/':
            endpoint = f'/{endpoint}'

        if not endpoint:
            return None
        elif endpoint[0] != '/':
            endpoint = f'/{endpoint}'

        _url = f'{self._base_url}{endpoint}'

        if kwargs:
            _params = {
                k: str((1 if v else 0) if isinstance(v, bool) else v)
                for k, v in kwargs.items() if v is not None
            }
            if _params:
                _params = [f'{k}={urllib.parse.quote_plus(v)}' for k, v in _params.items()]
                _url = f'{_url}?{"&".join(_params)}'

        logging.debug(f'GET: {_url}')

        response = requests.get(
            _url,
            headers=self._headers,
            verify=self._cert_path
        )

        response.raise_for_status()

        return response.json()

    def generate_invoice(self, amount: float, memo: str = None, expiry=300) -> Optional[dict]:
        try:
            invoice = self._post('invoices', value=amount, memo=memo, expiry=expiry)
        except Exception as e:
            logging.debug(f'Exception: {e}', exc_info=True)
            return None

        return invoice

    def get_invoices(self, pending_only=False, index_offset=1, num_max_invoices=None, reversed=False) -> Optional[List[dict]]:
        try:
            invoices = self._get(
                'invoices',
                pending_only=pending_only,
                index_offset=index_offset,
                num_max_invoices=num_max_invoices,
                reversed=reversed
            )
        except Exception as e:
            logging.debug(f'Exception: {e}', exc_info=True)
            return None

        return invoices

    def get_invoice(self, r_hash) -> Optional[dict]:
        try:
            invoice = self._get(f'invoice/{base64.b64decode(r_hash).hex()}')
        except Exception as e:
            logging.debug(f'Exception: {e}', exc_info=True)
            return None

        return invoice

    def decode_payment_request(self, payment_request: str):
        try:
            result = self._get(f'payreq/{payment_request}')
        except Exception as e:
            logging.debug(f'Exception: {e}', exc_info=True)
            return None

        return result

    def pay_payment_request(self, payment_request: str):
        try:
            result = self._post('channels/transactions', payment_request=payment_request, fee_limit=5)
        except Exception as e:
            logging.debug(f'Exception: {e}', exc_info=True)
            return None

        return result


lnd: LND = LND()
