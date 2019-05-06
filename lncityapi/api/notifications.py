
import json

from flask_login import login_required, current_user

from lncityapi import app

from lncityapi.controllers.notificationscontroller import get_notifications_count, get_notifications, see_notifications

from lncityapi.other.util import route_prefix_v1


@app.route(route_prefix_v1 + '/notifications/count', methods=['GET'])
@login_required
def get_notifications_count_request():

    return json.dumps(get_notifications_count(current_user))


@app.route(route_prefix_v1 + '/notifications/get/<int:page>/<int:count>', methods=['GET'])
@login_required
def get_notifications_request(page, count):

    total = get_notifications_count(current_user).get('total')
    serializable_notifications = [n.serializable() for n in get_notifications(current_user, page, count)]

    see_notifications(current_user)

    return json.dumps({
        'page': page,
        'count': count,
        'total': total,
        'notifications': serializable_notifications
    })
