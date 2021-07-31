
from lncityapi import db
from lncityapi.models import BaseModel, Blog


class Tag(BaseModel):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(64), nullable=False)
    title = db.Column('title', db.String(64), nullable=False)
    blog_id = db.Column('blog_id', db.ForeignKey(Blog.id), nullable=False)

    blog = db.relationship('Blog', foreign_keys='Tag.blog_id', lazy='select')

    _fields = {
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
