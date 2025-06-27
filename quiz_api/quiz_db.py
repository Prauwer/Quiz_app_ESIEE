import sqlite3
from models import Question, PossibleAnswer
# On importe les deux sérialiseurs BDD -> Objet
from serializers import db_row_to_question, db_row_to_answer

DATABASE_NAME = 'Database.db'

def add_question_with_answers(question: Question):
    """Ajoute une question ET ses réponses dans la BDD en une seule transaction."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO questions (position, title, text, image) VALUES (?, ?, ?, ?)",
            (question.position, question.title, question.text, question.image)
        )
        question_id = cursor.lastrowid
        answers_to_insert = [
            (answer.text, 1 if answer.is_correct else 0, question_id) 
            for answer in question.possibleAnswers
        ]
        cursor.executemany(
            "INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)",
            answers_to_insert
        )
        conn.commit()
        return question_id
    except sqlite3.Error:
        conn.rollback() 
        return None
    finally:
        conn.close()

def question_exists(question_id: int):
    """Vérifie si une question avec un ID donné existe."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM questions WHERE id = ?", (question_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def is_position_conflicting(position: int, question_id: int):
    """Vérifie si la position est déjà utilisée par une AUTRE question."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM questions WHERE position = ? AND id != ?", (position, question_id))
    conflict = cursor.fetchone() is not None
    conn.close()
    return conflict

def update_question_with_answers(question_id: int, question: Question):
    """
    Met à jour une question et ses réponses dans la BDD.
    Retourne 1 en cas de succès, -1 si la position est déjà utilisée, 0 si la question n'existe pas.
    """
    if not question_exists(question_id):
        return 0 # La question n'existe pas

    if is_position_conflicting(question.position, question_id):
        return -1 # Conflit de position

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE questions 
               SET position = ?, title = ?, text = ?, image = ?
               WHERE id = ?""",
            (question.position, question.title, question.text, question.image, question_id)
        )
        
        cursor.execute("DELETE FROM possible_answers WHERE question_id = ?", (question_id,))
        if question.possibleAnswers:
            answers_to_insert = [
                (answer.text, 1 if answer.is_correct else 0, question_id) 
                for answer in question.possibleAnswers
            ]
            cursor.executemany(
                "INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)",
                answers_to_insert
            )
        conn.commit()
        return 1 # Succès
    except sqlite3.Error as e:
        print(f"Erreur inattendue lors de la mise à jour: {e}")
        conn.rollback()
        return 0 
    finally:
        conn.close()

def get_answers_for_question(question_id: int):
    """Récupère toutes les réponses possibles pour une question donnée."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM possible_answers WHERE question_id = ?", (question_id,))
    rows = cursor.fetchall()
    conn.close()
    return [db_row_to_answer(row) for row in rows]

def get_question_by_id(question_id: int):
    """Récupère une question par son ID et retourne un objet Question complet avec ses réponses."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    row = cursor.fetchone()
    conn.close()
    question = db_row_to_question(row)
    if question:
        question.possibleAnswers = get_answers_for_question(question.id)
    return question

def get_question_by_position(position: int):
    """Récupère une question par sa position et retourne un objet Question complet avec ses réponses."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE position = ?", (position,))
    row = cursor.fetchone()
    conn.close()
    question = db_row_to_question(row)
    if question:
        question.possibleAnswers = get_answers_for_question(question.id)
    return question

def get_question_count():
    """Retourne le nombre total de questions dans le quiz."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def delete_all_questions():
    """Supprime toutes les questions et réponses de la base de données."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM possible_answers")
        cursor.execute("DELETE FROM questions")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('questions', 'possible_answers')")
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
    finally:
        conn.close()

def delete_question_by_id(question_id: int):
    """Supprime une question spécifique et ses réponses par son ID."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    deleted_count = 0
    try:
        cursor.execute("DELETE FROM possible_answers WHERE question_id = ?", (question_id,))
        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        deleted_count = cursor.rowcount
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
    finally:
        conn.close()
    return deleted_count