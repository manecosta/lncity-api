
import binascii, hashlib, uuid, arrow

from typing import Tuple, Union, Optional

from lncityapi.models import User, Userauthtoken, Userrefreshtoken, Spamblock
from lncityapi.other.util import random_string

from lncityapi import db


# Helper methods

def _hash_password(password, salt) -> str:
    return binascii.hexlify(
        hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 126349)
    ).decode('utf-8')


def _new_refresh_token(seed: str) -> str:
    return binascii.hexlify(
        hashlib.pbkdf2_hmac('sha256', seed.encode('utf-8'), uuid.uuid4().bytes, 113245)
    ).decode('utf-8')


def _new_auth_token() -> str:
    return uuid.uuid4().hex + uuid.uuid4().hex


def _get_login_spam_block(username: str):
    sb = None
    for _sb in Spamblock.query.filter_by(key=f'login[username={username}]'):
        if _sb.expired_time > arrow.get().timestamp():
            sb = _sb
        else:
            _sb.delete_instance()
    return sb


def _increment_login_spam_block(username: str):
    sb = _get_login_spam_block(username)
    if sb is None:
        sb = Spamblock(
            count=1,
            key=f'login[username={username}]',
            expired_time=arrow.get().shift(minutes=10).timestamp()
        )

        db.session.add(sb)
        db.session.commit()
    else:
        if sb.count <= 5:
            sb.count = sb.count + 1
        sb.expired_time = arrow.get().shift(minutes=sb.count * 10).timestamp()

        db.session.commit()

    return sb


def _clear_expired_login_spam_block():
    Spamblock.query.filter(Spamblock.expired_time < arrow.get().timestamp()).delete()
    db.session.commit()


# Login / Register

def login(login_request: dict) -> Tuple[int, Union[str, dict]]:
    username = login_request.get('username')
    password = login_request.get('password')
    refresh_token = login_request.get('refresh_token')

    expire_auth_tokens()
    expire_refresh_tokens()
    _clear_expired_login_spam_block()

    if username is not None and password is not None:

        sb = _get_login_spam_block(username)
        if sb is not None:
            if sb.count > 5:
                _increment_login_spam_block(username)
                return 429, 'Too many attempts. Try again in a while.'

        _user = get_user_by_username(username)
        if _user is None:
            return 401, 'Invalid credentials'

        _passhash = _user.passhash
        _salt = _user.salt
        if _passhash is None or _salt is None:
            # This is kind of a weird scenario that shouldn't happen
            # A user that has username but no password makes no sense, but it's still here for sanity
            return 401, 'Invalid credentials'

        _test_passhash = _hash_password(password, _salt)

        _refresh_token = generate_refresh_token(_user)
        _auth_token = generate_auth_token(_user)

        if _test_passhash == _passhash:
            return 200, {
                'user': _user,
                'auth_token': _auth_token,
                'refresh_token': _refresh_token
            }
        else:
            _increment_login_spam_block(username)
            return 401, 'Invalid credentials'

    elif refresh_token is not None:
        _user = get_user_by_refresh_token(refresh_token)
        if _user is None:
            return 401, 'Invalid credentials'

        # For users that have not yet defined a username and password we always keep the same non expiring refresh token
        if _user.passhash is None:
            _refresh_token = refresh_token
        else:
            _refresh_token = generate_refresh_token(_user)

        _auth_token = generate_auth_token(_user)

        return 200, {
            'user': _user,
            'auth_token': _auth_token,
            'refresh_token': _refresh_token
        }

    else:
        return 400, 'Please provide either username/password or refresh_token'


def register_user() -> dict:
    _user = User(
        balance=0,
        created_time=arrow.get().timestamp(),
        updated_time=arrow.get().timestamp()
    )

    db.session.add(_user)
    db.session.commit()
    db.session.refresh(_user)

    _auth_token = generate_auth_token(_user)
    _refresh_token = generate_refresh_token(_user)

    return {
        'user': _user,
        'auth_token': _auth_token,
        'refresh_token': _refresh_token
    }


def add_username_and_password(user: User, add_credentials_request: dict) -> Tuple[int, Union[str, dict]]:

    _username = add_credentials_request.get('username')
    _password = add_credentials_request.get('password')

    _collision_user = get_user_by_username(_username)

    if _collision_user is not None and _collision_user.id != user.id:
        return 409, 'Username already taken'

    _salt = random_string()
    user.username = _username
    user.passhash = _hash_password(_password, _salt)
    user.salt = _salt

    user.updated_time = arrow.get().timestamp()
    db.session.commit()

    delete_user_auth_tokens(user)
    delete_user_refresh_tokens(user)

    _auth_token = generate_auth_token(user)
    _refresh_token = generate_refresh_token(user)

    return 200, {
        'user': user,
        'auth_token': _auth_token,
        'refresh_token': _refresh_token
    }


# Token management

def delete_user_refresh_tokens(user: User):
    Userrefreshtoken.query.filter_by(user_id=user.id).delete()
    db.session.commit()


def delete_user_auth_tokens(user: User):
    Userauthtoken.query.filter_by(user_id=user.id).delete()
    db.session.commit()


def delete_refresh_token(refresh_token: str):
    Userrefreshtoken.query.filter_by(refresh_token=refresh_token).delete()
    db.session.commit()


def generate_refresh_token(user: User):
    _refresh_token = _new_refresh_token(user.passhash if user.passhash is not None else random_string())

    _expired_time = arrow.get().shift(days=30).timestamp()
    if user.passhash is None:
        # If the user has no passhash we set the refresh token to virtually never expire
        _expired_time = arrow.get().shift(years=100).timestamp()

    _userrefreshtoken = Userrefreshtoken(
        user_id=user.id,
        refresh_token=_refresh_token,
        expired_time=_expired_time
    )

    db.session.add(_userrefreshtoken)
    db.session.commit()

    return _refresh_token


def generate_auth_token(user: User):
    _auth_token = _new_auth_token()

    _expired_time = arrow.get().shift(hours=1).timestamp()

    _userauthtoken = Userauthtoken(
        user_id=user.id,
        auth_token=_auth_token,
        expired_time=_expired_time
    )

    db.session.add(_userauthtoken)
    db.session.commit()

    return _auth_token


def expire_refresh_tokens():
    Userrefreshtoken.query.filter(Userrefreshtoken.expired_time < arrow.get().timestamp()).delete()
    db.session.commit()


def expire_auth_tokens():
    Userauthtoken.query.filter(Userauthtoken.expired_time < arrow.get().timestamp()).delete()
    db.session.commit()


# Gets

def get_user_by_refresh_token(refresh_token: str):
    for urt in Userrefreshtoken.query.join(User, Userrefreshtoken.user_id == User.id)\
            .filter(Userrefreshtoken.refresh_token == refresh_token)\
            .filter(Userrefreshtoken.expired_time > arrow.get().timestamp()):
        return urt.user

    return None


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()


def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_auth_token(auth_token: str, add_auth_properties=False):
    for uat in Userauthtoken.query.join(User, Userauthtoken.user_id == User.id)\
            .filter(Userauthtoken.auth_token == auth_token)\
            .filter(Userauthtoken.expired_time > arrow.get().timestamp()):
        _user = uat.user

        if add_auth_properties:
            setattr(_user, 'is_authenticated', True)
            setattr(_user, 'is_active', True)
            setattr(_user, 'is_anonymous', False)

        return _user

    return None
