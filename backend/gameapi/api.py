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
import time
from dateutil import parser
from dateutil.tz import UTC
import pytz
from functools import wraps
from flask import Blueprint, jsonify, request, Response, redirect
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
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
                return jsonify(dict(message="Can't recognize user stored in token",
                                    authenticated=False)), 401
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError) as e:
            # TODO: Use logger
            print(e)
            return jsonify(invalid_msg), 401
        except (Exception) as e:
            # TODO: Use logger
            print(e)
            return jsonify(dict(message="Backend error",
                                authenticated=False)), 401

    return _verify

@api.route('/register', methods=['POST'])
@token_required
@login_required
def register(jwt_user):
    if jwt_user.id != current_user.id:
        # User ID stored in JWT token does not match the one stored in session
        # It's better to re-authenticate
        return jsonify(dict(message='Re-authentication required', registered=False)), 401

    data = request.get_json()
    username = data['username']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        # Generate random string containing 8 characters
        password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        user = User(username, password)
        try:
            db.session.add(user)
            db.session.commit()

            return jsonify(dict(message='Register successfully',
                                registered=True,
                                user_data=dict(id=user.id,
                                               username=username,
                                               password=password,
                                               role=user.role))), 201
        except (SQLAlchemyError) as e:
            # TODO: Use logger
            print(e)
            return jsonify(dict(message='Register failed', registered=False)), 500
    else:
        return jsonify(dict(message='User existed', registered=False)), 400

@api.route('/reset_password', methods=['POST'])
@token_required
@login_required
def reset_password(jwt_user):
    if jwt_user.id != current_user.id:
        # User ID stored in JWT token does not match the one stored in session
        # It's better to re-authenticate
        return jsonify(dict(message='Re-authentication required', registered=False)), 401

    # Only admin has permission to reset password
    if current_user.role != 'admin':
        return jsonify(dict(message='Permission denied', registered=False)), 403

    data = request.get_json()
    username = data['username']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is not None:
        # Generate random string containing 8 characters
        password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        registered_user.password = password_hash
        try:
            db.session.commit()

            return jsonify(dict(message='Reset successfully',
                                registered=True,
                                user_data=dict(id=registered_user.id,
                                               username=username,
                                               password=password,
                                               role=registered_user.role))), 201
        except (SQLAlchemyError) as e:
            # TODO: Use logger
            print(e)
            return jsonify(dict(message='Reset failed', registered=False)), 500
    else:
        return jsonify(dict(message='User doesn\'t exist', registered=False)), 400

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, password) == False:
        return jsonify(dict(message='Username or password is invalid', authenticated=False)), 401

    registered_user.last_login_at = datetime.utcnow()
    try:
        db.session.add(registered_user)
        db.session.commit()
    except:
        pass

    if login_user(registered_user):
        token = jwt.encode({
            'sub': registered_user.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig().SECRET_KEY)

        return jsonify(dict(message='Logged in successfully',
                            authenticated=True,
                            token=token.decode('utf-8'),
                            user_data=dict(user_id=registered_user.id,
                                           username=registered_user.username,
                                           role=registered_user.role,
                                           last_login_at=int(registered_user.last_login_at.timestamp())))), 200
    else:
        return jsonify(dict(message='Logged in failed', authenticated=False)), 500

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
        return jsonify(dict(message='Re-authentication required')), 401

    r = requests.get(url=WC_URL)

    matches = []
    rounds = r.json()['rounds']
    if rounds:
        for aRound in rounds:
            if aRound['matches'] and len(aRound['matches']) > 0:
                matches = matches + aRound['matches']

    if len(matches) > 0:
        for m in matches:
            match_time_str = m['date'] + ' ' + m['time'] + ' ' + (m['timezone'] if m['timezone'] else '')
            match_time = parser.parse(match_time_str)
            match_time = match_time.replace(tzinfo=pytz.utc) + match_time.utcoffset()
            m['match_time_utc_seconds'] = int(match_time.timestamp())
            

        # Sort matches by match time
        matches = sorted(matches,
                         key=lambda m: m['match_time_utc_seconds'], reverse=False
                        )

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
        return jsonify(dict(message='Re-authentication required')), 401

    predictions = Prediction.query.filter(Prediction.user_id == jwt_user).all()
    return jsonify([p.to_dict() for p in predictions]), 200

@api.route('/submit_prediction', methods=['POST'])
@token_required
@login_required
def submit_prediction(jwt_user):
    if jwt_user.id != current_user.id:
        return jsonify(dict(message='Re-authentication required')), 401

    data = request.get_json()
    match_id = data['match_id']
    prediction = data['prediction']

    # Do not allow update prediction if the match started
    current_time = int(time.time())

    r = requests.get(url=WC_URL)
    match = None
    matches = []
    rounds = r.json()['rounds']
    if rounds:
        for aRound in rounds:
            if aRound['matches'] and len(aRound['matches']) > 0:
                matches = matches + aRound['matches']
    for m in matches:
        if m['num'] == match_id:
            match = m
    if match:
        match_time_str = match['date'] + ' ' + match['time'] + ' ' + (match['timezone'] if match['timezone'] else '')
        match_time = parser.parse(match_time_str)
        match_time = match_time.replace(tzinfo=pytz.utc) + match_time.utcoffset()
        match_time = int(match_time.timestamp())
        diff = match_time - current_time
        print('diff=%d' % diff)

        if diff <= 0:
            return jsonify(dict(message='Not enough time to predict',
                                submitted=False)), 400
    else:
        return jsonify(dict(message='Match doesn\'t exist',
                            submitted=False)), 400

    p = Prediction.query.filter(Prediction.user_id == jwt_user.id).filter(Prediction.match_id == match_id).first()
    try:
        if p:
            p.prediction = prediction
            db.session.commit()
        else:
            p = Prediction(user_id=jwt_user.id, match_id=match_id, prediction=prediction)
            db.session.add(p)
            db.session.commit()

        return jsonify(dict(message='Submit prediction successfully',
                            submitted=True,
                            data=p.to_dict())), 201
    except (SQLAlchemyError) as e:
        # TODO: Use logger
        print(e)
        return jsonify(dict(message='Submit prediction failed',
                            submitted=False), 500)
