
import json

from flask_login import login_required

from lncityapi import app
from lncityapi.controllers.tagscontroller import get_tags
from lncityapi.other.util import route_prefix_v1


@app.route(route_prefix_v1 + '/tags/get', methods=['GET'])
def get_tags_request():

    tags = get_tags()

    return json.dumps({
        'tags': [tag.serializable() for tag in tags]
    })
