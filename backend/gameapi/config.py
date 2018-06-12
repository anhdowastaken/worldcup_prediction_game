"""
config.py
- Settings for the flask application object
"""

class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///game.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # String is used for encryption and session management
    SECRET_KEY = 'mysecretkey'
