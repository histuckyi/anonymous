from flask import Flask
from config import flask_config


def create_app():
    app = Flask(__name__)
    app.config.from_object((get_flask_env()))
    return app


def get_flask_env():
    if flask_config.Config.ENV == 'DEV':
        return 'config.flask_config.devConfig'
    else:
        return 'config.flask_config.devConfig'
