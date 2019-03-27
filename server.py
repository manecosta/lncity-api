
import json

from flask import Flask, abort, request

from services.lnd import LND

route_prefix_v1 = '/api/v1'

app = Flask(__name__)

lnd = LND()


@app.route(route_prefix_v1 + '/invoices/generate/<float:amount>/<str:memo>', method='GET')
@app.route(route_prefix_v1 + '/invoices/generate/<float:amount>')
def generate_invoice_request(amount: float, memo: str = None):

    invoice = lnd.create_invoice(amount, memo)

    if invoice is not None:
        return json.dumps(invoice)
    else:
        abort(500, 'Unable to generate a new invoice')


@app.route(route_prefix_v1 + '/invoices/get', methods=['POST'])
def get_invoice_request():
    body = request.json()

    r_hash = body.get('r_hash')

    if not r_hash:
        abort(400, 'Please provide \'r_hash\'')

    invoice = lnd.get_invoice(r_hash)

    if invoice is None:
        abort(404, 'Invoice not found')

    return json.dumps(invoice)


if __name__ == '__main__':
    app.run(host='ln.city', port=5001)
