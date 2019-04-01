
import json
import logging

from flask import request, abort
from werkzeug.exceptions import HTTPException

from lncityapi import app, loginManager
from lncityapi.controllers.userscontroller import get_user_by_auth_token
from lncityapi.other.common import lncity_db

from conf import conf


@loginManager.request_loader
def load_user_from_request_aux(request):
    auth_token = request.headers.get('X-Auth-Token')
    return get_user_by_auth_token(auth_token, add_auth_properties=True)


@app.before_request
def before_request():
    lncity_db.connect()

    if request.headers.get('Content-Type') != 'application/json':
        abort(415, 'Unsupported Content Type')


@app.after_request
def after_request(response):
    lncity_db.close()

    if response.status == '200 OK':
        if response.headers.get('Content-Type', {}) == 'text/html; charset=utf-8':
            response.headers['Content-Type'] = 'application/json'

    response.headers['X-Server-Version'] = conf.get('VERSION')
    response.headers['X-Request-Id'] = request.headers.get('X-Request-ID', '')

    return response


@app.errorhandler(Exception)
def handle_exception_error(e: Exception):
    if isinstance(e, HTTPException):
        return e.description, e.code

    if request.method == 'GET':
        return '500 - Internal Server Error', 500

    if request.json is not None:
        request_body = request.json
    elif request.form is not None:
        request_body = json.dumps(request.form)
    else:
        request_body = {}

    logging.exception(f'500 - Internal Server Error. ExceptionType: {repr(e)}. RequestBody: {request_body}.')

    return '500 - Internal Server Error', 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
