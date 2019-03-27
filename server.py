
import json

from flask import Flask, abort

from services.lnd_service import LNDService

app = Flask(__name__)

lnd_service = LNDService()


@app.route('/invoices/generate/<float:amount>/<str:memo>', method='GET')
@app.route('/invoices/generate/<float:amount>')
def generate_invoice_request(amount: float, memo: str = None):

    invoice = lnd_service.invoices_new(amount, memo)

    if invoice is not None:
        return json.dumps(invoice)
    else:
        abort(500, 'Unable to generate a new invoice')
