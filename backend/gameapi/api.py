"""
api.py
- Provide the API endpoints for consuming and producing
  REST requests and responses
"""

import json
import requests
import random
import string
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, jsonify, request, Response, redirect
from flask_login import current_user, login_user, logout_user, login_required
import jwt
from .application import bcrypt
from .config import BaseConfig
from .models import db, User, Prediction

WC_URL = 'https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json'
api = Blueprint('api', __name__)

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Re-authentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, BaseConfig().SECRET_KEY)
            user = User.query.filter_by(id=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

@api.route('/register', methods=['POST'])
@token_required
@login_required
def register(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Authentication required'), registered=False), 400

    data = request.get_json()
    username = data['username']
    # Generate random string containing 8 characters
    password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    return jsonify(dict(message='Register successfully',
                        registered=True,
                        user_data=dict(id=user.id, username=username, password=password, role=user.role))), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, password) == False:
        return jsonify(dict(message='Username or password is invalid', authenticated=False)), 401

    registered_user.last_login_at = datetime.utcnow()
    db.session.add(registered_user)
    db.session.commit()
    login_user(registered_user)

    token = jwt.encode({
        'sub': registered_user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig().SECRET_KEY)

    return jsonify(dict(message='Logged in successfully',
                        authenticated=True,
                        token=token.decode('utf-8'),
                        user_data=dict(user_id=registered_user.id, role=registered_user.role, last_login_at=registered_user.last_login_at))), 200

@api.route('/logout', methods=['POST'])
def logout():
    logout_user()

    return jsonify(dict(message='Logged out successfully')), 200

@api.route('/get_matches/', methods=['GET'])
def get_matches():
    r = requests.get(url=WC_URL)

    matches = []
    rounds = r.json()['rounds']
    if rounds:
        for aRound in rounds:
            if aRound['matches'] and len(aRound['matches']) > 0:
                matches = matches + aRound['matches']

    # The URL above return a json object
    # We're going to prepare Flask response
    json_response = json.dumps(matches)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers.add('content-length', len(json_response))
    response.status_code=200

    return response

@api.route('/get_matches_with_prediction', methods=['GET'])
@token_required
@login_required
def get_matches_with_predictions(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Authentication required')), 400

    r = requests.get(url=WC_URL)

    matches = []
    rounds = r.json()['rounds']
    if rounds:
        for aRound in rounds:
            if aRound['matches'] and len(aRound['matches']) > 0:
                matches = matches + aRound['matches']

    if len(matches) > 0:
        predictions = Prediction.query.filter(Prediction.user_id == jwt_user.id).all()
        for p in predictions:
            for m in matches:
                if m['num'] == p.match_id:
                    m['prediction'] = p.prediction
                    break

    # The URL above return a json object
    # We're going to prepare Flask response
    json_response = json.dumps(matches)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers.add('content-length', len(json_response))
    response.status_code=200

    return response

@api.route('/get_predictions', methods=['GET'])
@token_required
@login_required
def get_predictions(jwt_user):
    if jwt_user != current_user.id:
        return jsonify(dict(message='Authentication required')), 400

    predictions = Prediction.query.filter(Prediction.user_id == jwt_user).all()
    return jsonify([p.to_dict() for p in predictions]), 200

@api.route('/submit_prediction', methods=['POST'])
@token_required
@login_required
def submit_prediction(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Authentication required')), 400

    data = request.get_json()
    match_id = data['match_id']
    prediction = data['prediction']

    p = Prediction.query.filter(Prediction.user_id == jwt_user.id).filter(Prediction.match_id == match_id).first()
    if p:
        p.prediction = prediction
        db.session.commit()
    else:
        p = Prediction(user_id=jwt_user.id, match_id=match_id, prediction=prediction)
        db.session.add(p)
        db.session.commit()

    return jsonify(p.to_dict()), 201
