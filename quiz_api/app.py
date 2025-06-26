from flask import Flask, request
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a1b9f8c7e6d5a4b3c2d1f0e9d8c7b6a5a4b3c2d1f0e9'
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    # Le hash MD5 du mot de passe 'iloveflask'
    admin_password_hash = 'd278077bbfe7285a144d4b5b11adb9cf'

    if payload and 'password' in payload:
        # Convertir le mot de passe reçu en MD5
        password_from_request = payload['password']
        hashed_password = hashlib.md5(password_from_request.encode()).hexdigest()

        # Comparer les hashs
        if hashed_password == admin_password_hash:
            token = jwt.encode({
                'exp' : datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return {"token": token}, 200
            
    return 'Unauthorized', 401

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()
