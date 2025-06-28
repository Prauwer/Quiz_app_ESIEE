import sqlite3
import json
from datetime import datetime
from models import Question, PossibleAnswer, Participation
from serializers import db_row_to_question, db_row_to_answer

DATABASE_NAME = 'Database.db'

def rebuild_database():
    """Supprime et recrée toutes les tables pour une base de données propre."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS participations")
        cursor.execute("DROP TABLE IF EXISTS possible_answers")
        cursor.execute("DROP TABLE IF EXISTS questions")
        cursor.execute("""
            CREATE TABLE questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position INTEGER NOT NULL UNIQUE,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                image TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE possible_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                is_correct INTEGER NOT NULL CHECK(is_correct IN (0, 1)),
                question_id INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        """)
        cursor.execute("""
            CREATE TABLE participations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                answers TEXT NOT NULL,
                score INTEGER,
                date TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la reconstruction de la base de données : {e}")
        conn.rollback()
    finally:
        conn.close()


def _get_question_position(cursor, question_id: int):
    """Récupère la position actuelle d'une question."""
    cursor.execute("SELECT position FROM questions WHERE id = ?", (question_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def _get_max_question_position(cursor):
    """Récupère la position maximale actuellement dans le quiz."""
    cursor.execute("SELECT MAX(position) FROM questions")
    result = cursor.fetchone()[0]
    return result if result is not None else 0

def _shift_positions_down(cursor, from_position: int):
    """Décale les positions de 1 vers le bas, de manière compatible."""
    cursor.execute("SELECT id FROM questions WHERE position >= ? ORDER BY position DESC", (from_position,))
    ids_to_update = [row[0] for row in cursor.fetchall()]
    for q_id in ids_to_update:
        cursor.execute("UPDATE questions SET position = position + 1 WHERE id = ?", (q_id,))

def _shift_positions_up(cursor, from_position: int):
    """Décale les positions de 1 vers le haut, de manière plus robuste."""
    cursor.execute("SELECT id FROM questions WHERE position > ? ORDER BY position ASC", (from_position,))
    ids_to_update = [row[0] for row in cursor.fetchall()]
    for q_id in ids_to_update:
        cursor.execute("UPDATE questions SET position = position - 1 WHERE id = ?", (q_id,))

def add_question_with_answers(question: Question):
    """Ajoute une question, comble les trous de position et décale les autres si nécessaire."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        max_pos = _get_max_question_position(cursor)
        if question.position > max_pos + 1:
            question.position = max_pos + 1

        _shift_positions_down(cursor, question.position)
        cursor.execute(
            "INSERT INTO questions (position, title, text, image) VALUES (?, ?, ?, ?)",
            (question.position, question.title, question.text, question.image)
        )
        question_id = cursor.lastrowid
        answers_to_insert = [(answer.text, 1 if answer.is_correct else 0, question_id) for answer in question.possibleAnswers]
        cursor.executemany("INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)", answers_to_insert)
        conn.commit()
        return question_id
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la question: {e}")
        conn.rollback() 
        return None
    finally:
        conn.close()

def update_question_with_answers(question_id: int, question_data: Question):
    """Met à jour une question et gère le réordonnancement des autres."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        old_position = _get_question_position(cursor, question_id)
        if old_position is None:
            return 0
        new_position = question_data.position
        if old_position == new_position:
            cursor.execute("UPDATE questions SET title = ?, text = ?, image = ? WHERE id = ?", (question_data.title, question_data.text, question_data.image, question_id))
        else:
            cursor.execute("UPDATE questions SET position = -1 WHERE id = ?", (question_id,))
            if new_position < old_position:
                cursor.execute("SELECT id FROM questions WHERE position >= ? AND position < ? ORDER BY position DESC", (new_position, old_position))
                ids_to_shift = [row[0] for row in cursor.fetchall()]
                for q_id in ids_to_shift:
                    cursor.execute("UPDATE questions SET position = position + 1 WHERE id = ?", (q_id,))
            else:
                cursor.execute("SELECT id FROM questions WHERE position > ? AND position <= ? ORDER BY position ASC", (old_position, new_position))
                ids_to_shift = [row[0] for row in cursor.fetchall()]
                for q_id in ids_to_shift:
                    cursor.execute("UPDATE questions SET position = position - 1 WHERE id = ?", (q_id,))
            cursor.execute("UPDATE questions SET position = ?, title = ?, text = ?, image = ? WHERE id = ?", (new_position, question_data.title, question_data.text, question_data.image, question_id))
        cursor.execute("DELETE FROM possible_answers WHERE question_id = ?", (question_id,))
        if question_data.possibleAnswers:
            answers_to_insert = [(answer.text, 1 if answer.is_correct else 0, question_id) for answer in question_data.possibleAnswers]
            cursor.executemany("INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)", answers_to_insert)
        conn.commit()
        return 1
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()

def get_all_questions_and_answers():
    """Récupère toutes les questions et leurs réponses, ordonnées par position."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY position ASC")
    question_rows = cursor.fetchall()
    questions = []
    for q_row in question_rows:
        question = db_row_to_question(q_row)
        question.possibleAnswers = get_answers_for_question(question.id)
        questions.append(question)
    conn.close()
    return questions

def add_participation(participation: Participation):
    """Enregistre une nouvelle participation avec score et date."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        answers_json = json.dumps(participation.answers)
        participation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO participations (player_name, answers, score, date) VALUES (?, ?, ?, ?)",
            (participation.player_name, answers_json, participation.score, participation_date)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la participation: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_all_scores():
    """Récupère tous les scores, triés par score décroissant."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, score, date FROM participations ORDER BY score DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

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
    """Supprime une question et décale les autres."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        position = _get_question_position(cursor, question_id)
        if position is None:
            return 0
        cursor.execute("DELETE FROM possible_answers WHERE question_id = ?", (question_id,))
        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        _shift_positions_up(cursor, position)
        conn.commit()
        return 1
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la question {question_id}: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()

def delete_all_participations():
    """Supprime toutes les participations de la base de données."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM participations")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'participations'")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression des participations : {e}")
        conn.rollback()
    finally:
        conn.close()