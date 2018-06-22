# WORLD CUP PREDICTION GAME

Prediction game for World Cup

## 1. Backend

I'm using Flask with Python 3 to develop backend.
To work with backend, enter virtual environment first:

```bash
cd ./backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### 1.1. How to install backend

```bash
pip3 install --upgrade -r requirements.txt
```

### 1.2. How to manage db

```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

You can use shell to modify db such as adding admin account

```bash
python3 manage.py shell
```

### 1.2. How to run backend

```bash
python3 appserver.py
```

```bash
 * Serving Flask app "GAME_API" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 638-165-501
```

## 2. Frontend

I'm using VueJS to develop frontend

### 2.1. How to install frontend

```bash
cd ./frontend/worldcup_prediction_game_spa
npm install
```

### 2.2. How to run frontend

```bash
npm run dev
```

```bash
 I  Your application is running here: http://localhost:8080
```
