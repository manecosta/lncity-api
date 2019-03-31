
import binascii, hashlib, uuid

from datetime import datetime, timedelta

from typing import Tuple, Union, Optional

from lncityapi.models import User, Userauthtoken, Userrefreshtoken
from lncityapi.other.util import random_string


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


# Login / Register

def login(login_request) -> Tuple[int, Union[str, dict]]:
    username = login_request.get('username')
    password = login_request.get('password')
    refresh_token = login_request.get('refresh_token')

    if username is not None and password is not None:
        _user = get_user_by_username(username)
        if _user is None:
            return 401, 'Invalid credentials'

        _passhash = _user.passhash
        _salt = _user.salt
        if _passhash is None or _salt is None:
            return 401, 'Invalid credentials'

        _test_passhash = _hash_password(password, _salt)

        _refresh_token = generate_refresh_token(_user)
        _auth_token = generate_auth_token(_user)

        expire_auth_tokens()
        expire_refresh_tokens()

        if _test_passhash == _passhash:
            return 200, {
                'user': _user,
                'auth_token': _auth_token,
                'refresh_token': _refresh_token
            }
        else:
            return 401, 'Invalid credentials'

    elif refresh_token is not None:
        _user = get_user_by_refresh_token(refresh_token)
        if _user is None:
            return 401, 'Invalid credentials'

        # For users that have not yet defined a username and password we always keep the same non expiring refresh token
        if _user.passhash is None:
            _refresh_token = refresh_token
        else:
            delete_refresh_token(refresh_token)
            _refresh_token = generate_refresh_token(_user)

        _auth_token = generate_auth_token(_user)

        return 200, {
            'user': _user,
            'auth_token': _auth_token,
            'refresh_token': _refresh_token
        }

    else:
        return 400, 'Please provide either username/password or refresh_token.'


def register_user() -> dict:
    _user = User.create(
        balance=0,
        created=datetime.now(),
        updated=datetime.now()
    )

    _auth_token = generate_auth_token(_user)
    _refresh_token = generate_refresh_token(_user)

    return {
        'user': _user,
        'auth_token': _auth_token,
        'refresh_token': _refresh_token
    }


def add_username_and_password(user: User, username, password):
    _salt = random_string()
    user.username = username
    user.passhash = _hash_password(password, _salt)
    user.salt = _salt

    user.updated = datetime.now()
    user.save()

    delete_user_auth_tokens(user)
    delete_user_refresh_tokens(user)

    _auth_token = generate_auth_token(user)
    _refresh_token = generate_refresh_token(user)

    return {
        'user': user,
        'auth_token': _auth_token,
        'refresh_token': _refresh_token
    }


# Token management

def delete_user_refresh_tokens(user: User):
    Userrefreshtoken.delete().where(Userrefreshtoken.user == user.id).execute()


def delete_user_auth_tokens(user: User):
    Userauthtoken.delete().where(Userauthtoken.user == user.id).execute()


def delete_refresh_token(refresh_token: str):
    Userrefreshtoken.delete().where(Userrefreshtoken.refresh_token == refresh_token).execute()


def generate_refresh_token(user: User):
    _refresh_token = _new_refresh_token(user.passhash if user.passhash is not None else random_string())

    _expiration_date = datetime.now() + timedelta(days=30)
    if user.passhash is None:
        # If the user has no passhash we set the refresh token to virtually never expire
        _expiration_date = datetime.now() + timedelta(days=100*365)

    Userrefreshtoken.create(
        user=user.id,
        refresh_token=_refresh_token,
        expiration_date=_expiration_date
    )

    return _refresh_token


def generate_auth_token(user: User):
    _auth_token = _new_auth_token()

    _expiration_date = datetime.now() + timedelta(hours=1)

    Userrefreshtoken.create(
        user=user.id,
        auth_token=_auth_token,
        expiration_date=_expiration_date
    )

    return _auth_token


def expire_refresh_tokens():
    Userrefreshtoken.delete().where(Userrefreshtoken.expiration_date < datetime.now()).execute()


def expire_auth_tokens():
    Userauthtoken.delete().where(Userauthtoken.expiration_date < datetime.now()).execute()


# Gets

def get_user_by_refresh_token(refresh_token: str) -> Optional[User]:
    for urt in Userrefreshtoken.select(Userrefreshtoken, User)\
            .join(User).where(Userrefreshtoken.refresh_token == refresh_token,
                              Userrefreshtoken.expiration_date > datetime.now()):
        return urt.user

    return None


def get_user_by_username(username: str) -> Optional[User]:
    for u in User.select().where(User.username == username):
        return u

    return None


def get_user_by_auth_token(auth_token: str) -> Optional[User]:
    for uat in Userauthtoken.select(Userauthtoken, User)\
            .join(User).where(Userauthtoken.auth_token == auth_token,
                              Userauthtoken.expiration_date > datetime.now()):
        return uat.user

    return None

