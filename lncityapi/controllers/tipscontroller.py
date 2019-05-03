
import logging

from flask_login import current_user

from lncityapi.controllers.balancescontroller import add_user_balance
from lncityapi.controllers.blogscontroller import get_blog_post,get_blog_post_comment
from lncityapi.controllers.userscontroller import get_user, get_user_by_username
from lncityapi.controllers.logscontroller import add_log

from lncityapi.models.blog import Blogpost, Blogpostcomment


def tip_target(target, amount):

    try:
        target_components = target.split('/')

        if target_components[0] == 'lncity':

            success = add_user_balance(current_user, -amount)

            if not success:
                return 412, 'Not enough balance'

        elif target_components[0] == 'blogpost':
            blogpost_id = int(target_components[1])
            blogpost: Blogpost = get_blog_post(blogpost_id)
            if blogpost is None:
                return 404, 'Target not found'

            success = add_user_balance(current_user, -amount)

            if not success:
                return 412, 'Not enough balance'

            add_user_balance(blogpost.user, amount)

            blogpost.donation_amount += amount
            blogpost.donation_count += 1
            blogpost.save()

        elif target_components[0] == 'blogpostcomment':

            blogpostcomment_id = int(target_components[1])
            blogpostcomment: Blogpostcomment = get_blog_post_comment(blogpostcomment_id)
            if blogpostcomment is None:
                return 404, 'Target not found'

            success = add_user_balance(current_user, -amount)

            if not success:
                return 412, 'Not enough balance'

            add_user_balance(blogpostcomment.user, amount)

            blogpostcomment.donation_amount += amount
            blogpostcomment.donation_count += 1
            blogpostcomment.save()

        elif target_components[0] == 'user':

            try:
                user_id = int(target_components[1])
                user = get_user(user_id)
            except Exception as e:
                username = str(target_components[1])
                logging.info(username)
                user = get_user_by_username(username)

            if user is None:
                return 404, 'Target not found'

            success = add_user_balance(current_user, -amount)

            if not success:
                return 412, 'Not enough balance'

            add_user_balance(user, amount)

        else:
            return 400, 'Unrecognizable target'
    except Exception as e:
        logging.exception(e)
        return 400, 'Malformed target'

    add_log(current_user.id, None, 'tip', {'target': target, 'amount': amount})

    return 200, 'Ok'
