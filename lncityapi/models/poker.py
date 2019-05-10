
from peewee import ForeignKeyField, DoubleField, CharField, IntegerField

from lncityapi.models import BaseModel, JSONField, User


class Pokerhand(BaseModel):
    identifier = CharField(max_length=32, null=False)
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    info = JSONField(null=False)
    multiplier = IntegerField(null=False)
    time = DoubleField(null=False)
    settled = IntegerField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'identifier': {
                'type': 'model',
                'show': True
            },
            'user': {
                'type': 'model',
                'show': False
            },
            'info': {
                'type': 'base',
                'show': True
            },
            'multiplier': {
                'type': 'base',
                'show': True
            },
            'time': {
                'type': 'base',
                'show': True
            },
            'settled': {
                'type': 'base',
                'show': False
            },
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'pokerhand'
