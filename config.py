import os


DEBUG = False

AUTH_TOKEN_KEY_URL = os.getenv('AUTH_TOKEN_KEY_URL', '')

JWT_DECODE_AUDIENCE = 'trusted-app'


def get_role(dict):
    return dict.get('authorities')


JWT_ROLE_CLAIM = get_role

VERIFY_CERT = True


