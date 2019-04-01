
from marshmallow import Schema, fields


class UserLoginRequest(Schema):
    username = fields.Str(required=False, missing=None)
    password = fields.Str(required=False, missing=None)
    refresh_token = fields.Str(required=False, missing=None)


class UserAddCredentialsRequest(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
