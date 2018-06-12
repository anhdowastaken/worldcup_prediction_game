"""
application.py
- Create a Flask app instance and register the database object
"""

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .models import User

login_manager = LoginManager()
# login_manager.login_view = 'api.login'

def create_app(app_name='GAME_API'):
    app = Flask(app_name)
    app.config.from_object('gameapi.config.BaseConfig')
    app.config['TESTING'] = False
    app.config['LOGIN_DISABLED'] = False

    cors = CORS(app, resource={r"/api/*": {"origin": "*"}})

    from gameapi.api import api
    app.register_blueprint(api, url_prefix='/api')

    from gameapi.models import db
    db.init_app(app)

    login_manager.init_app(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    user = User.query.filter(User.id == user_id).first()
    return user
