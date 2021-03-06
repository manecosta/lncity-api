
from peewee import CharField

from lncityapi.models import BaseModel


class Game(BaseModel):
    name = CharField(max_length=64, null=False)
    title = CharField(max_length=128, null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'name': {
                'type': 'base',
                'show': True
            },
            'title': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'game'
