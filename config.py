import os

DEBUG = False

# The following four variables configure authentication

# If using a JWK Set, set the environment variable AUTH_JWKS_URL to the url where it can be retrieved
AUTH_JWKS_URL = os.getenv('oauth_server_jwks_url')

# If using a public key, set the environment variable AUTH_TOKEN_KEY_URL to the url where it can be retrieved
AUTH_TOKEN_KEY_URL = os.getenv('oauth_server_token_key_url')

# Set the path to the certificate for AUTH_JWKS_URL/AUTH_TOKEN_KEY_URL. If set to False then, SSL verification will not occur.
AUTH_CERT_PATH = os.getenv('oauth_server_cert_path', True)

# If using the above, use the AUTH_TOKEN_KEY_ALGORITHM to set the algorithm. By default it will be RS256
JWT_ALGORITHM = os.getenv('jwt_algorithm', 'HS256')

# Set the JWT_DECODE_AUDIENCE environment variable to the value of the 'aud' claim in the
JWT_DECODE_AUDIENCE = os.getenv('jwt_decode_audience')

# Configure exception JSON to not always output with a `message` field. Global exception handling is done via a custom handler in services.py.
ERROR_INCLUDE_MESSAGE=False

#Configure the maximum number of transactions that can be submitted in a single ddot file.
MAXIMUM_TRANSACTIONS=os.getenv('maximum_transactions', '15000')
