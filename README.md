# worldcup_prediction_game
Prediction game for World Cup

# How to run backend
cd ./backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade -r requirements.txt
python3 appserver.py

# How to run frontend
cd ./frontend/worldcup_prediction_game_spa
npm install
npm run dev

# db
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade

python3 manage.py shell