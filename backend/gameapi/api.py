"""
api.py
- Provide the API endpoints for consuming and producing
  REST requests and responses
"""

import json
import requests
from flask import Blueprint, jsonify, request, Response, redirect
from flask_login import current_user, login_user, logout_user, login_required
from .models import db, User, Prediction

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(data['username'], data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(dict(message='Register successfully')), 201
 
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return jsonify(dict(message='Username or password is invalid')), 401

    login_user(registered_user)

    return jsonify(dict(message='Logged in successfully')), 200

@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()

    return jsonify(dict(message='Logged out successfully')), 200

@api.route('/get_matches/', methods=['GET'])
def get_matches():
    r = requests.get(url='https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json')

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

@api.route('/get_matches_with_prediction/user_id/<int:user_id>', methods=['GET'])
@login_required
def get_matches_with_predictions(user_id):
    if user_id != current_user.id:
        return jsonify(dict(message='Authentication required')), 400

    r = requests.get(url='https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json')

    matches = []
    rounds = r.json()['rounds']
    if rounds:
        for aRound in rounds:
            if aRound['matches'] and len(aRound['matches']) > 0:
                matches = matches + aRound['matches']

    if len(matches) > 0:
        predictions = Prediction.query.filter(Prediction.user_id == user_id).all()
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

@api.route('/get_predictions/user_id/<int:user_id>', methods=['GET'])
@login_required
def get_predictions(user_id):
    if user_id != current_user.id:
        return jsonify(dict(message='Authentication required')), 400

    predictions = Prediction.query.filter(Prediction.user_id == user_id).all()
    return jsonify([p.to_dict() for p in predictions]), 200

@api.route('/submit_prediction', methods=['POST'])
@login_required
def submit_prediction():
    data = request.get_json()
    user_id = data['user_id']
    if user_id != current_user.id:
        return jsonify(dict(message='Authentication required')), 400

    match_id = data['match_id']
    prediction = data['prediction']

    p = Prediction.query.filter(Prediction.user_id == user_id).filter(Prediction.match_id == match_id).first()
    if p:
        p.prediction = prediction
        db.session.commit()
    else:
        p = Prediction(user_id=user_id, match_id=match_id, prediction=prediction)
        db.session.add(p)
        db.session.commit()

    return jsonify(p.to_dict()), 201
