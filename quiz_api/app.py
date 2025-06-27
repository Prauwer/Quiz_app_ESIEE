from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import hashlib
import quiz_db
from serializers import json_to_question, question_to_json
from models import Participation

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
            token = jwt.encode({'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
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
            return jsonify({"error": "Erreur lors de la création de la question"}), 500

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

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db_endpoint():
    """Supprime et recrée la base de données."""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Jeton d'autorisation manquant"}), 401
    
    quiz_db.rebuild_database()
    return "Ok", 200

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
        else:
            return jsonify({"error": "La question à mettre à jour n'a pas été trouvée ou une erreur est survenue"}), 404

@app.route('/participations', methods=['POST'])
def create_participation():
    """Crée une nouvelle participation et retourne le score."""
    data = request.get_json()
    if not data or not all(k in data for k in ['playerName', 'answers']):
        return jsonify({"error": "Données manquantes : playerName et answers sont requis"}), 400

    player_name = data.get('playerName')
    player_answers_positions = data.get('answers')
    all_questions = quiz_db.get_all_questions_and_answers()

    if len(player_answers_positions) != len(all_questions):
        return jsonify({"error": "Le nombre de réponses ne correspond pas au nombre de questions"}), 400

    score = 0
    answers_summary = []
    for i, question in enumerate(all_questions):
        correct_answer_position = -1
        correct_answer_id = None
        was_correct = False
        for ans_idx, answer in enumerate(question.possibleAnswers):
            if answer.is_correct:
                correct_answer_position = ans_idx + 1
                correct_answer_id = answer.id
                break
        player_chosen_position = -1
        try:
            player_chosen_position = int(player_answers_positions[i])
        except (ValueError, TypeError):
             player_chosen_position = -1
        if player_chosen_position > 0 and player_chosen_position == correct_answer_position:
            score += 1
            was_correct = True
        answers_summary.append({"correctAnswerId": correct_answer_id, "wasCorrect": was_correct})
    
    participation = Participation(player_name, player_answers_positions, score)
    quiz_db.add_participation(participation)
    
    return jsonify(participation.to_json_summary(answers_summary)), 200


@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations_endpoint():
    """Supprime toutes les participations enregistrées."""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Jeton d'autorisation manquant"}), 401
    
    quiz_db.delete_all_participations()
    return '', 204

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    """Retourne des informations générales sur le quiz et les scores passés."""
    size = quiz_db.get_question_count()
    scores_from_db = quiz_db.get_all_scores()
    
    formatted_scores = []
    for score_entry in scores_from_db:
        try:
            # Parse la date stockée en BDD (format YYYY-MM-DD HH:MM:SS)
            date_obj = datetime.strptime(score_entry['date'], '%Y-%m-%d %H:%M:%S')
            # Formate la date comme demandé (dd/MM/yyyy HH:mm:ss)
            formatted_date = date_obj.strftime('%d/%m/%Y %H:%M:%S')
            formatted_scores.append({
                "playerName": score_entry['player_name'],
                "score": score_entry['score'],
                "date": formatted_date
            })
        except (ValueError, TypeError):
            # Gère le cas où la date serait null ou mal formatée en BDD
            formatted_scores.append({
                "playerName": score_entry['player_name'],
                "score": score_entry['score'],
                "date": "Date invalide"
            })
            
    return jsonify({"size": size, "scores": formatted_scores}), 200

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()