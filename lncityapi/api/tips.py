
import json

from flask import abort, request
from flask_login import login_required

from lncityapi import app
from lncityapi.controllers.tipscontroller import tip_target
from lncityapi.other.util import route_prefix_v1


@app.route(route_prefix_v1 + '/tips/send', methods=['POST'])
@login_required
def send_tip_request():

    payload = request.get_json()

    target = payload.get('target')
    amount = payload.get('amount')

    if target is None or amount is None:
        return 400, 'Provide a target and an amount'

    if amount <= 0:
        return 400, 'Provide a valid amount'

    code, result = tip_target(target, amount)

    if code != 200:
        abort(code, result)

    return json.dumps(result)
