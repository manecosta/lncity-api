
from peewee import CharField, IntegerField, ForeignKeyField, DoubleField

from lncityapi.models import BaseModel


class User(BaseModel):
    username = CharField(max_length=64, null=True)
    passhash = CharField(max_length=64, null=True)
    salt = CharField(max_length=32, null=True)
    balance = DoubleField(null=False, default=0)
    created_time = DoubleField(null=False)
    updated_time = DoubleField(null=False)
    deleted = IntegerField(null=False, default=0)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'id': {
                'type': 'base',
                'show': True
            },
            'username': {
                'type': 'base',
                'show': True
            },
            'balance': {
                'type': 'base',
                'show': False
            },
            'created_time': {
                'type': 'base',
                'show': True
            },
            'updated_time': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'user'


class Userauthtoken(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User)
    auth_token = CharField(max_length=64, null=False)
    expired_time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': False
            },
            'auth_token': {
                'type': 'base',
                'show': True
            },
            'expired_time': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'userauthtoken'


class Userrefreshtoken(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User)
    refresh_token = CharField(max_length=64, null=False)
    expired_time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': False
            },
            'refresh_token': {
                'type': 'base',
                'show': True
            },
            'expired_time': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'userrefreshtoken'
