
from peewee import ForeignKeyField, CharField, DoubleField

from lncityapi.models import BaseModel, JSONField, User, Game


class Log(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    game = ForeignKeyField(column_name='game_id', field='id', model=Game, null=True)
    event = CharField(max_length=64, null=False)
    info = JSONField(null=False)
    time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'game': {
                'type': 'model',
                'show': True
            },
            'event': {
                'type': 'base',
                'show': True
            },
            'info': {
                'type': 'base',
                'show': True
            },
            'time': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'log'
