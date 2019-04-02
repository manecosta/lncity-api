
import json

from flask import abort, request
from flask_login import login_required, current_user

from conf import conf
from lncityapi import app
from lncityapi.controllers.balancescontroller import try_update_balance_with_deposit_invoice
from lncityapi.services.lnd import lnd
from lncityapi.other.util import route_prefix_v1


@app.route(route_prefix_v1 + '/invoices/generate/<int:amount>/<string:memo>', methods=['GET'])
@app.route(route_prefix_v1 + '/invoices/generate/<int:amount>')
@login_required
def generate_invoice_request(amount: float, memo: str = None):

    invoice = lnd.generate_invoice(amount, memo, conf.get('INVOICE_TIMEOUT'))

    if invoice is not None:
        return json.dumps(invoice)
    else:
        abort(500, 'Unable to generate a new invoice')


@app.route(route_prefix_v1 + '/invoices/get', methods=['POST'])
@login_required
def get_invoice_request():
    body = request.get_json()

    r_hash = body.get('r_hash')

    if not r_hash:
        abort(400, 'Please provide \'r_hash\'')

    invoice = lnd.get_invoice(r_hash)

    if invoice is None:
        abort(404, 'Invoice not found')

    if invoice.get('settled', False):
        deposited = try_update_balance_with_deposit_invoice(r_hash)
        if deposited:
            invoice['deposited'] = True

    return json.dumps(invoice)
