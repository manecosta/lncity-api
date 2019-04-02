
from marshmallow import Schema, fields


class DepositBalanceRequest(Schema):
    amount = fields.Integer(required=True)


class WithdrawBalanceRequest(Schema):
    invoice = fields.Str(required=True)
