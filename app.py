import os

from flask import Flask

application = Flask(__name__)

application.config.from_object('config')

if os.path.exists('.env'):
    application.config.from_pyfile('.env')

from services import *

if __name__ == '__main__':
    application.run()