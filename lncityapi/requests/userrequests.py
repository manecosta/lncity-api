
from marshmallow import Schema, fields


class UserLoginRequest(Schema):
    username = fields.Str(required=False)
    password = fields.Str(required=False)
    refresh_token = fields.Str(required=False)


class UserAddCredentialsRequest(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
