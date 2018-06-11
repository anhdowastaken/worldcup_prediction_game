"""
api.py
- Provide the API endpoints for consuming and producing
  REST requests and responses
"""

import json
import requests
from flask import Blueprint, jsonify, request, Response
from .models import db, User, Prediction

api = Blueprint('api', __name__)

@api.route('/get_matches/')
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

@api.route('/get_matches_with_prediction/user_id/<int:user_id>')
def get_matches_with_predictions(user_id):
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

@api.route('/get_predictions/user_id/<int:user_id>')
def get_predictions(user_id):
    predictions = Prediction.query.filter(Prediction.user_id == user_id).all()
    return jsonify([p.to_dict() for p in predictions])

@api.route('/submit_prediction', methods=['POST'])
def submit_prediction():
    data = request.get_json()
    user_id = data['user_id']
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
