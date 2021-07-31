
from lncityapi import db
from lncityapi.models import BaseModel, User
from sqlalchemy_jsonfield import JSONField


class Pokerhand(BaseModel):
    __tablename__ = 'pokerhand'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column('identifier', db.String(32), nullable=False)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    info = db.Column('info', JSONField(enforce_string=True, enforce_unicode=False), nullable=False)
    multiplier = db.Column('multiplier', db.Integer, nullable=False)
    time = db.Column('time', db.Float, nullable=False)
    settled = db.Column('settled', db.Integer, nullable=False, default=0)

    user = db.relationship('User', foreign_keys='Pokerhand.user_id', lazy='select')

    _fields = {
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
