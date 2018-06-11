"""
application.py
- Create a Flask app instance and register the database object
"""

from flask import Flask

def create_app(app_name='GAME_API'):
    app = Flask(app_name)
    app.config.from_object('gameapi.config.BaseConfig')
    from gameapi.api import api
    app.register_blueprint(api, url_prefix='/api')
    return app
