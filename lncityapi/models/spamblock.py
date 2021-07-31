
from lncityapi import db
from lncityapi.models import BaseModel


class Spamblock(BaseModel):
    __tablename__ = 'spamblock'

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column('count', db.Integer, nullable=False, default=0)
    key = db.Column('key', db.String(128), nullable=False)
    expired_time = db.Column('expired_time', db.Float, nullable=True)
