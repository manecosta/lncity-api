
from peewee import ForeignKeyField, CharField, DoubleField, IntegerField

from lncityapi.models import BaseModel, JSONField, User


class Notification(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    other_user = ForeignKeyField(column_name='other_user_id', field='id', model=User, null=True)
    event = CharField(max_length=64, null=False)
    info = JSONField(null=False)
    seen = IntegerField(null=False)
    time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'other_user': {
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
            'seen': {
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
        table_name = 'notification'
