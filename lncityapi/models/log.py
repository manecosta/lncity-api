
from lncityapi import db
from lncityapi.models import BaseModel, User, Game
from sqlalchemy_jsonfield import JSONField


class Log(BaseModel):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id))
    game_id = db.Column('game_id', db.ForeignKey(Game.id), nullable=True)
    event = db.Column('event', db.String(64), nullable=False)
    info = db.Column('info', JSONField(enforce_string=True, enforce_unicode=False), nullable=False)
    time = db.Column('time', db.Float, nullable=False)

    user = db.relationship('User', foreign_keys='Log.user_id', lazy='select')
    game = db.relationship('Game', foreign_keys='Log.game_id', lazy='select')

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
