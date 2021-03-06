from typing import Dict, Union


from peewee import ForeignKeyField, CharField, DoubleField, TextField

from lncityapi.models import BaseModel, User, Tag


class Blog(BaseModel):
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    title = CharField(max_length=128, null=False)
    created_time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'title': {
                'type': 'base',
                'show': True
            },
            'created_time': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'blog'


class Blogpost(BaseModel):
    blog = ForeignKeyField(column_name='blog_id', field='id', model=Blog, null=False)
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    title = CharField(max_length=128, null=False)
    body = TextField(null=False)
    created_time = DoubleField(null=False)
    updated_time = DoubleField(null=False)
    donation_count = DoubleField(null=False, default=0)
    donation_amount = DoubleField(null=False, default=0)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'id': {
                'type': 'base',
                'show': True
            },
            'user': {
                'type': 'model',
                'show': True
            },
            'blog': {
                'type': 'model',
                'show': False
            },
            'tags': {
                'type': 'model',
                'show': True
            },
            'title': {
                'type': 'base',
                'show': True
            },
            'body': {
                'type': 'base',
                'show': True
            },
            'created_time': {
                'type': 'base',
                'show': True
            },
            'updated_time': {
                'type': 'base',
                'show': True
            },
            'donation_count': {
                'type': 'base',
                'show': True
            },
            'donation_amount': {
                'type': 'base',
                'show': True
            },
            'comments_count': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'blogpost'


class Blogposttag(BaseModel):
    blogpost = ForeignKeyField(column_name='blogpost_id', field='id', model=Blogpost, null=False)
    tag = ForeignKeyField(column_name='tag_id', field='id', model=Tag, null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'id': {
                'type': 'base',
                'show': True
            },
            'blogpost': {
                'type': 'model',
                'show': True
            },
            'tag': {
                'type': 'model',
                'show': False
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'blogposttag'


class Blogpostdonation(BaseModel):
    blogpost = ForeignKeyField(column_name='blogpost_id', field='id', model=Blogpost, null=False)
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    amount = DoubleField(null=False)
    time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'blogpost': {
                'type': 'model',
                'show': False
            },
            'amount': {
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
        table_name = 'blogpostdonation'


class Blogpostcomment(BaseModel):
    blogpost = ForeignKeyField(column_name='blogpost_id', field='id', model=Blogpost, null=False)
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    body = TextField(null=False)
    created_time = DoubleField(null=False)
    donation_count = DoubleField(null=False, default=0)
    donation_amount = DoubleField(null=False, default=0)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'id': {
                'type': 'base',
                'show': True
            },
            'user': {
                'type': 'model',
                'show': True
            },
            'blogpost': {
                'type': 'model',
                'show': False
            },
            'body': {
                'type': 'base',
                'show': True
            },
            'created_time': {
                'type': 'base',
                'show': True
            },
            'donation_count': {
                'type': 'base',
                'show': True
            },
            'donation_amount': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)

    class Meta:
        table_name = 'blogpostcomment'


class Blogpostcommentdonation(BaseModel):
    blogpostcomment = ForeignKeyField(column_name='blogpostcomment_id', field='id', model=Blogpostcomment, null=False)
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=False)
    amount = DoubleField(null=False)
    time = DoubleField(null=False)

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'blogpostcomment': {
                'type': 'model',
                'show': False
            },
            'amount': {
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
        table_name = 'blogpostcommentdonation'
