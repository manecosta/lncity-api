
from time import time

from peewee import JOIN

from lncityapi.models import Notification, User


def add_notification(user, other_user, event, info, seen=False):
    Notification.create(
        user=user.id,
        other_user=other_user.id if other_user else None,
        event=event,
        info=info,
        seen=seen,
        time=int(time())
    )


def see_notifications(user):
    return Notification.update(seen=1)\
        .where(Notification.user == user.id).execute()


def get_notifications_count(user):
    return {
        'total': Notification.select().where(Notification.user == user.id).count(),
        'unseen': Notification.select().where(Notification.user == user.id, Notification.seen == 0).count()
    }


def get_notifications(user, page, count):

    OtherUser = User.alias()

    query = (
        Notification.select(Notification, User, OtherUser)
            .join(User, JOIN.INNER, on=(Notification.user == User.id))
            .switch(Notification)
            .join(OtherUser, JOIN.LEFT_OUTER, on=(Notification.other_user == OtherUser.id))
            .where(Notification.user == user.id)
            .order_by(Notification.time.desc())
            .paginate(page, count)
    )

    notifications = []
    for n in query:
        notifications.append(n)

    return notifications
