
import json, arrow

from lncityapi.models import Log


def add_log(user_id, game_id, event, info, time=None):

    try:
        log = Log.create(
            user=user_id,
            game=game_id,
            event=event,
            info=json.dumps(info) if info is not None else '{}',
            time=arrow.get(time).timestamp
        )
    except Exception as e:
        return None

    return log
