
import json

from flask import abort, request
from flask_login import login_required, current_user
from marshmallow import ValidationError

from conf import conf
from lncityapi import app
from lncityapi.controllers.notificationscontroller import add_notification
from lncityapi.other.util import route_prefix_v1
from lncityapi.requests.balancerequests import DepositBalanceRequest, WithdrawBalanceRequest
from lncityapi.controllers.balancescontroller import generate_deposit_invoice_for_user, expire_deposit_invoices, \
    withdraw_balance_for_user


@app.route(route_prefix_v1 + '/balances/deposit', methods=['POST'])
@login_required
def deposit_account_balance_request():
    try:
        deposit_balance_request: DepositBalanceRequest = DepositBalanceRequest().load(request.get_json())
    except ValidationError as ve:
        return abort(400, json.dumps(ve.messages))

    expire_deposit_invoices()

    min_balance_movement = conf.get('MIN_BALANCE_MOVEMENT')
    max_balance_movement = conf.get('MAX_BALANCE_MOVEMENT')

    if deposit_balance_request.get('amount') > max_balance_movement or \
            deposit_balance_request.get('amount') < min_balance_movement:
        abort(412, f'Invalid amount. Please deposit between {min_balance_movement} and {max_balance_movement}')

    code, response = generate_deposit_invoice_for_user(current_user, deposit_balance_request.get('amount'))

    if code != 200:
        abort(code, response)

    return json.dumps(response)


@app.route(route_prefix_v1 + '/balances/withdraw', methods=['POST'])
def withdraw_account_balance_request():
    try:
        withdraw_balance_request: WithdrawBalanceRequest = WithdrawBalanceRequest().load(request.get_json())
    except ValidationError as ve:
        return abort(400, json.dumps(ve.messages))

    code, message = withdraw_balance_for_user(current_user, withdraw_balance_request.get('payment_request'))

    if code != 200:
        abort(code, message)

    return json.dumps({
        'message': message
    })
