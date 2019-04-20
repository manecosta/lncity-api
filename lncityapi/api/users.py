
import json

from flask import abort, request, Response
from flask_login import login_required, current_user
from marshmallow import ValidationError

from lncityapi import app
from lncityapi.other.util import route_prefix_v1
from lncityapi.requests.userrequests import UserLoginRequest, UserAddCredentialsRequest
from lncityapi.controllers.userscontroller import login, register_user, add_username_and_password
from lncityapi.controllers.balancescontroller import verify_pending_deposits_for_user
from lncityapi.models import User


@app.route(route_prefix_v1 + '/users/register', methods=['POST'])
def register_user_request():
    result = register_user()

    user: User = result.get('user')
    auth_token: str = result.get('auth_token')
    refresh_token: str = result.get('refresh_token')

    response = Response(json.dumps(user.serializable(fields={'balance': True})), 200)

    response.headers['Access-Control-Expose-Headers'] = 'X-Auth-Token, X-Refresh-Token'
    response.headers['X-Auth-Token'] = auth_token
    response.headers['X-Refresh-Token'] = refresh_token

    return response


@app.route(route_prefix_v1 + '/users/login', methods=['POST'])
def user_login_request():
    try:
        login_request = UserLoginRequest().load(request.get_json())
    except ValidationError as ve:
        return abort(400, json.dumps(ve.messages))

    code, result = login(login_request)

    if code != 200:
        abort(code, result)

    user: User = result.get('user')
    auth_token: str = result.get('auth_token')
    refresh_token: str = result.get('refresh_token')

    response = Response(json.dumps(user.serializable(fields={'balance': True})), 200)

    response.headers['Access-Control-Expose-Headers'] = 'X-Auth-Token, X-Refresh-Token'
    response.headers['X-Auth-Token'] = auth_token
    response.headers['X-Refresh-Token'] = refresh_token

    return response


@app.route(route_prefix_v1 + '/users/addcredentials', methods=['POST'])
@login_required
def add_user_credentials_request():
    try:
        add_credentials_request = UserAddCredentialsRequest().load(request.get_json())
    except ValidationError as ve:
        return abort(400, json.dumps(ve.messages))

    code, result = add_username_and_password(
        current_user, add_credentials_request
    )

    if code != 200:
        abort(code, result)

    user: User = result.get('user')
    auth_token: str = result.get('auth_token')
    refresh_token: str = result.get('refresh_token')

    response = Response(json.dumps(user.serializable(fields={'balance': True})), 200)

    response.headers['Access-Control-Expose-Headers'] = 'X-Auth-Token, X-Refresh-Token'
    response.headers['X-Auth-Token'] = auth_token
    response.headers['X-Refresh-Token'] = refresh_token

    return response


@app.route(route_prefix_v1 + '/users/me', methods=['GET'])
@login_required
def get_me_request():

    new_user = verify_pending_deposits_for_user(current_user)

    return json.dumps(new_user.serializable(fields={'balance': True}))
