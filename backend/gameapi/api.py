"""
api.py  
- Provide the API endpoints for consuming and producing
  REST requests and responses
"""

import json
import requests
from flask import Blueprint, jsonify, request, Response

api = Blueprint('api', __name__)

@api.route('/get/matches/')
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

