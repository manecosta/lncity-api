
from lncityapi.models import Tag


def get_tags():

    tags = []
    for tag in Tag.query.all():
        tags.append(tag)

    return tags
