
from lncityapi import db
from lncityapi.models import BaseModel


class Game(BaseModel):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(64), nullable=False)
    title = db.Column('title', db.String(128), nullable=False)

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
