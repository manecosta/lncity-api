
from peewee import CharField, DeferredForeignKey

from lncityapi.models import BaseModel


class Tag(BaseModel):
    name = CharField(max_length=64, null=False)
    title = CharField(max_length=64, null=False)
    blog = DeferredForeignKey('Blog', column_name='blog_id', field='id', null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'id': {
                'type': 'base',
                'show': True
            },
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
        table_name = 'tag'
