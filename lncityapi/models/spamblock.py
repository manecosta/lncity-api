
from peewee import IntegerField, CharField, DoubleField

from lncityapi.models import BaseModel


class Spamblock(BaseModel):
    count = IntegerField(null=False, default=0)
    key = CharField(max_length=128, null=False)
    expired_time = DoubleField(null=True)

    class Meta:
        table_name = 'spamblock'
