"""
application.py
- Create a Flask app instance and register the database object
"""

from flask import Flask
from flask_cors import CORS

def create_app(app_name='GAME_API'):
    app = Flask(app_name)
    app.config.from_object('gameapi.config.BaseConfig')

    cors = CORS(app, resource={r"/api/*": {"origin": "*"}})

    from gameapi.api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
