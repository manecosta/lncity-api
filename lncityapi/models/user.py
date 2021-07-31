
from lncityapi import db
from lncityapi.models import BaseModel


class User(BaseModel):
    __tablename__  = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(64), nullable=True)
    passhash = db.Column('passhash', db.String(64), nullable=True)
    salt = db.Column('salt', db.String(32), nullable=True)
    balance = db.Column('balance', db.Float, nullable=False, default=0)
    created_time = db.Column('created_time', db.Float, nullable=False)
    updated_time = db.Column('updated_time', db.Float, nullable=False)
    deleted = db.Column('deleted', db.Integer, nullable=False, default=0)

    _fields = {
        'id': {
            'type': 'base',
            'show': True
        },
        'username': {
            'type': 'base',
            'show': True
        },
        'balance': {
            'type': 'base',
            'show': False
        },
        'created_time': {
            'type': 'base',
            'show': True
        },
        'updated_time': {
            'type': 'base',
            'show': True
        }
    }
        


class Userauthtoken(BaseModel):
    __tablename__ = 'userauthtoken'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    auth_token = db.Column('auth_token', db.String(64), nullable=False)
    expired_time = db.Column('expired_time', db.Float, nullable=False)

    user = db.relationship('User', foreign_keys='Userauthtoken.user_id')

    _fields = {
        'user': {
            'type': 'model',
            'show': False
        },
        'auth_token': {
            'type': 'base',
            'show': True
        },
        'expired_time': {
            'type': 'base',
            'show': True
        }
    }
        


class Userrefreshtoken(BaseModel):
    __tablename__ = 'userrefreshtoken'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    refresh_token = db.Column('refresh_token', db.String(64), nullable=False)
    expired_time = db.Column('expired_time', db.Float, nullable=False)

    user = db.relationship('User', foreign_keys='Userrefreshtoken.user_id', lazy='select')

    _fields = {
        'user': {
            'type': 'model',
            'show': False
        },
        'refresh_token': {
            'type': 'base',
            'show': True
        },
        'expired_time': {
            'type': 'base',
            'show': True
        }
    }
