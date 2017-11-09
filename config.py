import os

DEBUG = False

# The following four variables configure authentication

# If using a public key, set the environment variable AUTH_TOKEN_KEY_URL to the url where it can be retrieved
AUTH_TOKEN_KEY_URL = os.getenv('auth_token_key_url')

# If using the above, use the AUTH_TOKEN_KEY_ALGORITHM to set the algorithm. By default it will be RS256
JWT_ALGORITHM = os.getenv('jwt_algorithm', 'HS256')

# Set the JWT_DECODE_AUDIENCE environment variable to the value of the 'aud' claim in the
JWT_DECODE_AUDIENCE = os.getenv('jwt_decode_audience')

# Define the function that retrieves the roles from the JWT and assign to JWT_ROLE_CLAIM.
def get_role(dict):
    return dict.get('authorities')
JWT_ROLE_CLAIM = get_role

# Set the path
AUTH_CERT_PATH = os.getenv('auth_cert_path', True)


