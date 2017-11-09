import os
import requests


from flask import Flask

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

if application.config.get('AUTH_TOKEN_KEY_URL'):
    resp = requests.get(application.config.get('AUTH_TOKEN_KEY_URL'), verify=application.config['VERIFY_CERT'])
    application.config['JWT_PUBLIC_KEY'] = resp.json()['value']
    application.config['JWT_ALGORITHM'] = 'RS256'

from services import *

if __name__ == '__main__':
    application.run()