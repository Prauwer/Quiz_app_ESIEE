from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import hashlib
import quiz_db
from serializers import json_to_question, question_to_json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a1b9f8c7e6d5a4b3c2d1f0e9d8c7b6a5a4b3c2d1f0e9'
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    admin_password_hash = '4f545f49354e135891e48f0898516135'
    if payload and 'password' in payload:
        password_from_request = payload['password']
        hashed_password = hashlib.md5(password_from_request.encode()).hexdigest()
        if hashed_password == admin_password_hash:
            token = jwt.encode({
                'exp' : datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return {"token": token}, 200
    return 'Unauthorized', 401


@app.route('/questions', methods=['POST'])
def post_question():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Jeton d'autorisation manquant"}), 401

    data = request.get_json()
    required_fields = ['position', 'title', 'text', 'possibleAnswers']
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Données manquantes. Les champs requis sont: " + ", ".join(required_fields)}), 400
    
    new_question = json_to_question(data)
    
    question_id = quiz_db.add_question_with_answers(new_question)

    if question_id:
        new_question.id = question_id
        return jsonify(question_to_json(new_question)), 200
    else:
        return jsonify({"error": "Impossible d'ajouter la question, la position existe peut-être déjà"}), 409


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()