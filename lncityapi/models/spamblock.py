
from peewee import IntegerField, DateTimeField, CharField

from lncityapi.models.basemodel import BaseModel


class Spamblock(BaseModel):
    count = IntegerField(null=False, default=0)
    expiration_date = DateTimeField(null=True)
    key = CharField(max_length=128, null=False)

    class Meta:
        table_name = 'spamblock'
