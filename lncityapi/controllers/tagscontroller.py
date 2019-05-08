
from lncityapi.models import Tag


def get_tags():

    tags = []
    for tag in Tag.select():
        tags.append(tag)

    return tags
