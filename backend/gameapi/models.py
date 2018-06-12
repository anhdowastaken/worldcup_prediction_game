"""
models.py
- Data classes for the gameapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    authenticated = db.Column(db.Boolean, default=False)

    def is_authenticated(self):
        # return self.authenticated
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def to_dict(self):
        return dict(id=self.id,
                    username=self.username,
                    authenticated=self.authenticated,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))

    def __repr__(self):
        return '[%d][%s][%s][%s]' % (self.id, self.username, self.authenticated, self.created_at.strftime('%Y-%m-%d %H:%M:%S'))

class Prediction(db.Model):
    __tablename__ = 'predictions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    match_id = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.Integer)

    def to_dict(self):
        return dict(user_id=self.user_id,
                    match_id=self.match_id,
                    prediction=self.prediction)
