import sqlite3
from models import Question, PossibleAnswer
from serializers import db_row_to_question

DATABASE_NAME = 'Database.db'

def add_question_with_answers(question: Question):
    """
    Ajoute une question ET ses réponses dans la BDD en une seule transaction.
    Retourne l'ID de la question si tout réussit.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Insertion de la question
        cursor.execute(
            "INSERT INTO questions (position, title, text, image) VALUES (?, ?, ?, ?)",
            (question.position, question.title, question.text, question.image)
        )
        question_id = cursor.lastrowid

        answers_to_insert = [
            (answer.text, 1 if answer.is_correct else 0, question_id) 
            for answer in question.possibleAnswers
        ]
        
        # Insertion de toutes les réponses
        cursor.executemany(
            "INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)",
            answers_to_insert
        )
        
        conn.commit()
        return question_id
    except sqlite3.IntegrityError:
        conn.rollback() 
        return None
    finally:
        conn.close()

def get_question_by_id(question_id: int):
    """Récupère une question par son ID et la retourne en tant qu'objet Question."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    row = cursor.fetchone()
    conn.close()

    return db_row_to_question(row)