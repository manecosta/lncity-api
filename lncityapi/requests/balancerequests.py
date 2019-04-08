
from marshmallow import Schema, fields


class DepositBalanceRequest(Schema):
    amount = fields.Integer(required=True)


class WithdrawBalanceRequest(Schema):
    payment_request = fields.Str(required=True)
