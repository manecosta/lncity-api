
from secrets import choice

route_prefix_v1 = '/api/v1'

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def random_string(length=32):
    return ''.join(choice(ALPHABET) for _ in range(length))
