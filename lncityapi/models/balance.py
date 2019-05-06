
from peewee import ForeignKeyField, CharField, IntegerField, DoubleField

from lncityapi.models import BaseModel, User


class Deposit(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    amount = DoubleField(null=False)
    r_hash = CharField(max_length=64, null=False)
    created_time = DoubleField(null=False)
    expired_time = DoubleField(null=True)
    settled = IntegerField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'amount': {
                'type': 'base',
                'show': True
            },
            'r_hash': {
                'type': 'base',
                'show': True
            },
            'created_time': {
                'type': 'base',
                'show': True
            },
            'expired_time': {
                'type': 'base',
                'show': True
            },
            'settled': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'deposit'


class Withdrawal(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False, unique=True)
    amount = DoubleField(null=False)
    created_time = DoubleField(null=False)
    settled = IntegerField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'amount': {
                'type': 'base',
                'show': True
            },
            'created_time': {
                'type': 'base',
                'show': True
            },
            'settled': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'withdrawal'
