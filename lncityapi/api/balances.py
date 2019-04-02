
import json

from flask import abort, request
from flask_login import login_required, current_user
from marshmallow import ValidationError

from conf import conf
from lncityapi import app
from lncityapi.other.util import route_prefix_v1
from lncityapi.requests.balancerequests import DepositBalanceRequest, WithdrawBalanceRequest
from lncityapi.controllers.balancescontroller import generate_deposit_invoice


@app.route(route_prefix_v1 + '/balances/deposit', methods=['POST'])
@login_required
def deposit_account_balance_request():
    try:
        deposit_balance_request: DepositBalanceRequest = DepositBalanceRequest().load(request.get_json())
    except ValidationError as ve:
        return abort(400, json.dumps(ve.messages))

    min_balance_movement = conf.get('MIN_BALANCE_MOVEMENT')
    max_balance_movement = conf.get('MAX_BALANCE_MOVEMENT')

    if deposit_balance_request.get('amount') > max_balance_movement or \
            deposit_balance_request.get('amount') < min_balance_movement:
        abort(412, f'Invalid amount. Please deposit between {min_balance_movement} and {max_balance_movement}')

    code, response = generate_deposit_invoice(current_user, deposit_balance_request.get('amount'))

    if code != 200:
        abort(code, response)

    return json.dumps(response)


@app.route(route_prefix_v1 + '/balances/withdraw', methods=['POST'])
def withdraw_account_balance_request():
    try:
        withdraw_balance_request = WithdrawBalanceRequest().load(request.get_json())
    except ValidationError as ve:
        return abort(400, json.dumps(ve.messages))

    return None
