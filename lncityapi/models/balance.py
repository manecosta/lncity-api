
from peewee import ForeignKeyField, CharField, IntegerField, DateField

from lncityapi.models.basemodel import BaseModel
from lncityapi.models import User


class Deposit(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    amount = IntegerField(null=False)
    r_hash = CharField(max_length=64, null=False)
    expiration_date = DateField(null=False)
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
            'expiration_date': {
                'type': 'date',
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
    amount = IntegerField(null=False)
    r_hash = CharField(max_length=64, null=True)
    expiration_date = DateField(null=False)

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
            'expiration_date': {
                'type': 'date',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'withdrawal'
