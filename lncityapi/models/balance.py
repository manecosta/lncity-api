
from lncityapi import db
from lncityapi.models import BaseModel, User


class Deposit(BaseModel):
    __tablename__ = 'deposit'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id))
    amount = db.Column('amount', db.Float, nullable=False)
    r_hash = db.Column('r_hash', db.String(64), nullable=False)
    created_time = db.Column('created_time', db.Float, nullable=False)
    expired_time = db.Column('expired_time', db.Float, nullable=False)
    settled = db.Column('settled', db.Integer, nullable=False, default=0)

    user = db.relationship('User', foreign_keys='Deposit.user_id', lazy='select')

    _fields = {
        'user': {
            'type': 'model',
            'show': True
        },
        'amount': {
            'type': 'base',
            'show': True
        },
        'r_hash': {
            'type': 'base',
            'show': True
        },
        'created_time': {
            'type': 'base',
            'show': True
        },
        'expired_time': {
            'type': 'base',
            'show': True
        },
        'settled': {
            'type': 'base',
            'show': True
        }
    }


class Withdrawal(BaseModel):
    __tablename__ = 'withdrawal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id), unique=True)
    amount = db.Column('amount', db.Float, nullable=False)
    created_time = db.Column('created_time', db.Float, nullable=False)
    settled = db.Column('settled', db.Integer, nullable=False, default=0)

    user = db.relationship('User', foreign_keys='Withdrawal.user_id', lazy='select')

    _fields = {
        'user': {
            'type': 'model',
            'show': True
        },
        'amount': {
            'type': 'base',
            'show': True
        },
        'created_time': {
            'type': 'base',
            'show': True
        },
        'settled': {
            'type': 'base',
            'show': True
        }
    }
