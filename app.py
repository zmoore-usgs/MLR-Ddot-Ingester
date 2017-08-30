import os

from flask import Flask

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

from services import *

if __name__ == '__main__':
    application.run()