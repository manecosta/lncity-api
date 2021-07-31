
from lncityapi import db
from lncityapi.models import BaseModel, User
from sqlalchemy_jsonfield import JSONField


class Notification(BaseModel):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey(User.id), nullable=False)
    other_user_id = db.Column('other_user_id', db.ForeignKey(User.id), nullable=True)
    event = db.Column('event', db.String(64), nullable=False)
    info = db.Column('info', JSONField(enforce_string=True, enforce_unicode=False), nullable=False)
    seen = db.Column('seen', db.Integer, nullable=False, default=0)
    time = db.Column('time', db.Float, nullable=False)

    user = db.relationship('User', foreign_keys='Notification.user_id', lazy='select')
    other_user = db.relationship('User', foreign_keys='Notification.other_user_id', lazy='select')

    def __init__(self, **kwargs):
        kwargs['fields'] = {
            'user': {
                'type': 'model',
                'show': True
            },
            'other_user': {
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
            'seen': {
                'type': 'base',
                'show': True
            },
            'time': {
                'type': 'base',
                'show': True
            }
        }
        super().__init__(**kwargs)
