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
    admin_password_hash = 'd278077bbfe7285a144d4b5b11adb9cf'
    if payload and 'password' in payload:
        password_from_request = payload['password']
        hashed_password = hashlib.md5(password_from_request.encode()).hexdigest()
        if hashed_password == admin_password_hash:
            token = jwt.encode({
                'exp' : datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return {"token": token}, 200
    return 'Unauthorized', 401


@app.route('/questions', methods=['GET', 'POST'])
def handle_questions():
    """Gère l'ajout d'une question ou la récupération par position."""
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Jeton d'autorisation manquant"}), 401
        data = request.get_json()
        required_fields = ['position', 'title', 'text', 'possibleAnswers']
        if not data or not all(k in data for k in required_fields):
            return jsonify({"error": "Données manquantes"}), 400
        new_question = json_to_question(data)
        question_id = quiz_db.add_question_with_answers(new_question)
        if question_id:
            new_question.id = question_id
            return jsonify(question_to_json(new_question)), 200
        else:
            return jsonify({"error": "La position existe peut-être déjà"}), 409

    elif request.method == 'GET':
        position = request.args.get('position')
        if not position:
            return jsonify({"error": "Paramètre 'position' manquant"}), 400
        try:
            question = quiz_db.get_question_by_position(int(position))
            if question:
                return jsonify(question_to_json(question)), 200
            else:
                return jsonify({"error": "Question non trouvée"}), 404
        except ValueError:
            return jsonify({"error": "Le paramètre 'position' doit être un entier"}), 400

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions_endpoint():
    """Supprime toutes les questions et réponses."""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Jeton d'autorisation manquant"}), 401
    quiz_db.delete_all_questions()
    return '', 204

@app.route('/questions/<int:question_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_question_by_id(question_id):
    """Gère la récupération, la suppression ou la mise à jour d'une question par son ID."""
    if request.method == 'GET':
        question = quiz_db.get_question_by_id(question_id)
        if question:
            return jsonify(question_to_json(question)), 200
        else:
            return jsonify({"error": "Question non trouvée"}), 404

    elif request.method == 'DELETE':
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Jeton d'autorisation manquant"}), 401
        deleted_count = quiz_db.delete_question_by_id(question_id)
        if deleted_count == 0:
            return jsonify({"error": "Question non trouvée"}), 404
        return '', 204
    
    elif request.method == 'PUT':
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Jeton d'autorisation manquant"}), 401
        
        data = request.get_json()
        updated_question_data = json_to_question(data)

        result = quiz_db.update_question_with_answers(question_id, updated_question_data)

        if result == 1:
            return '', 204
        elif result == -1:
            return jsonify({"error": "La position est déjà utilisée par une autre question"}), 409
        else:
            return jsonify({"error": "La question à mettre à jour n'a pas été trouvée"}), 404

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    """Retourne des informations générales sur le quiz."""
    size = quiz_db.get_question_count()
    # Les scores ne sont pas encore implémentés
    scores = []
    return jsonify({"size": size, "scores": scores}), 200

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()