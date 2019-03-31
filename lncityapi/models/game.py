
from peewee import CharField

from lncityapi.models.basemodel import BaseModel


class Game(BaseModel):
    name = CharField(max_length=64, null=False)
    title = CharField(max_length=128, null=False)

    def __init__(self):
        super().__init__({
            'name': {
                'type': 'base',
                'show': True
            },
            'title': {
                'type': 'base',
                'show': True
            }
        })

    class Meta:
        table_name = 'game'
