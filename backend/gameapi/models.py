"""
models.py
- Data classes for the gameapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .application import bcrypt

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '%d\t%s\t%s\t%s' % (self.id, self.username, self.password, self.last_login_at.strftime('%Y-%m-%d %H:%M:%S'))

    def to_dict(self):
        return dict(user_id=self.id,
                    username=self.username,
                    last_login_at=self.last_login_at)

class Prediction(db.Model):
    __tablename__ = 'predictions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    match_id = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.Integer)

    def __init__(self, user_id, match_id, prediction):
        self.user_id = user_id
        self.match_id = match_id
        self.prediction = prediction

    def __repr__(self):
        return '[%d] predicted [%d]: [%d]' % (self.user_id, self.match_id, self.prediction)

    def to_dict(self):
        return dict(user_id=self.user_id,
                    match_id=self.match_id,
                    prediction=self.prediction)
