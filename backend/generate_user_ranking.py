import requests
import copy
import json
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gameapi.models import User, Prediction

WC_URL = 'https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json'

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('gameapi.config.BaseConfig')
    db.init_app(app)

    return app

def main():
    app = create_app()
    app.app_context().push()

    with app.app_context():
        # Get matches from API
        r = requests.get(url=WC_URL)

        matches = []
        rounds = r.json()['rounds']
        if rounds:
            for aRound in rounds:
                if aRound['matches'] and len(aRound['matches']) > 0:
                    matches = matches + aRound['matches']

        if len(matches) > 0:
            # Get all users from db
            users = User.query.all()
            ranking = []

            for u in users:
                if u.role == 'admin':
                    continue

                record = dict(id=u.id, username=u.username)
                predictions = Prediction.query.filter(Prediction.user_id == u.id).all()

                matches_copy = copy.deepcopy(matches)

                # Append prediction of user to list of matches
                if len(predictions) > 0:
                    for p in predictions:
                        for m in matches_copy:
                            if m['num'] == p.match_id:
                                m['prediction'] = p.prediction
                                break

                # Calculate point
                point = 0
                for m in matches_copy:
                    if 'prediction' not in m:
                        prediction = None
                    else:
                        prediction = m['prediction']

                    score1 = m['score1']
                    if 'score1i' in m and m['score1i'] != None:
                        score1 = score1 + m['score1i']
                    if 'score1et' in m and m['score1et'] != None:
                        score1 = score1 + m['score1et']
                    if 'score1p' in m and m['score1p'] != None:
                        score1 = score1 + m['score1p']

                    score2 = m['score2']
                    if 'score2i' in m and m['score2i'] != None:
                        score2 = score2 + m['score2i']
                    if 'score2et' in m and m['score2et'] != None:
                        score2 = score2 + m['score2et']
                    if 'score2p' in m and m['score2p'] != None:
                        score2 = score2 + m['score2p']
 
                    if m['score1'] == None or m['score2'] == None:
                        continue
                    elif ((prediction == 0 and score1 == score2) or
                                 (prediction == 1 and score1 > score2) or
                                 (prediction == 2 and score1 < score2)):
                        continue
                    else:
                        point = point - 10

                record['point'] = point
                ranking.append(record)

            if len(ranking) > 0:
                # Sort
                ranking = sorted(ranking,
                    key=lambda r: r['point'], reverse=False
                )
                output = dict(time=int(time.time()), data=ranking)
                with open('ranking.json', 'w') as outfile:
                    json.dump(output, outfile)

if __name__ == '__main__':
    main()
