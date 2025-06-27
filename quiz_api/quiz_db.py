import sqlite3
from models import Question, PossibleAnswer
# On importe les deux sérialiseurs BDD -> Objet
from serializers import db_row_to_question, db_row_to_answer

DATABASE_NAME = 'Database.db'

def _get_question_position(cursor, question_id: int):
    """Récupère la position actuelle d'une question."""
    cursor.execute("SELECT position FROM questions WHERE id = ?", (question_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def _shift_positions_down(cursor, from_position: int):
    """Décale les positions de 1 vers le bas, de manière compatible avec toutes les versions de SQLite."""
    # On sélectionne les ID des questions à décaler, en les triant du plus grand au plus petit
    cursor.execute("SELECT id FROM questions WHERE position >= ? ORDER BY position DESC", (from_position,))
    # On récupère tous les IDs dans une liste
    ids_to_update = [row[0] for row in cursor.fetchall()]
    # On parcourt la liste et on met à jour chaque question individuellement
    # Cet ordre évite les conflits avec la contrainte UNIQUE
    for q_id in ids_to_update:
        cursor.execute("UPDATE questions SET position = position + 1 WHERE id = ?", (q_id,))

def _shift_positions_up(cursor, from_position: int):
    """Décale les positions de 1 vers le haut, de manière plus robuste."""
    # On sélectionne les ID des questions à décaler, en ordre croissant cette fois
    cursor.execute("SELECT id FROM questions WHERE position > ? ORDER BY position ASC", (from_position,))
    ids_to_update = [row[0] for row in cursor.fetchall()]
    # On met à jour chaque question individuellement pour éviter les conflits
    for q_id in ids_to_update:
        cursor.execute("UPDATE questions SET position = position - 1 WHERE id = ?", (q_id,))

def add_question_with_answers(question: Question):
    """Ajoute une question et décale les autres si nécessaire."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # On décale les questions existantes pour faire de la place
        _shift_positions_down(cursor, question.position)
        
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
    except sqlite3.Error as e:
        # Ajout d'un print pour faciliter le débogage
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
            return 0  # La question n'existe pas

        new_position = question_data.position
        
        # Si la position ne change pas, on fait une simple mise à jour
        if old_position == new_position:
            cursor.execute(
                """UPDATE questions SET title = ?, text = ?, image = ? WHERE id = ?""",
                (question_data.title, question_data.text, question_data.image, question_id)
            )
        else:
            # La position change, on gère le réordonnancement
            cursor.execute("UPDATE questions SET position = -1 WHERE id = ?", (question_id,))
            
            if new_position < old_position:
                # On décale vers le bas (incrémente la position) les questions affectées
                cursor.execute("SELECT id FROM questions WHERE position >= ? AND position < ? ORDER BY position DESC", (new_position, old_position))
                ids_to_shift = [row[0] for row in cursor.fetchall()]
                for q_id in ids_to_shift:
                    cursor.execute("UPDATE questions SET position = position + 1 WHERE id = ?", (q_id,))
            else: # new_position > old_position
                # On décale vers le haut (décrémente la position) les questions affectées
                cursor.execute("SELECT id FROM questions WHERE position > ? AND position <= ? ORDER BY position ASC", (old_position, new_position))
                ids_to_shift = [row[0] for row in cursor.fetchall()]
                for q_id in ids_to_shift:
                    cursor.execute("UPDATE questions SET position = position - 1 WHERE id = ?", (q_id,))

            # On met à jour la question cible avec toutes ses données, y compris sa nouvelle position
            cursor.execute(
                """UPDATE questions SET position = ?, title = ?, text = ?, image = ? WHERE id = ?""",
                (new_position, question_data.title, question_data.text, question_data.image, question_id)
            )

        # Mise à jour des réponses (on les remplace complètement)
        cursor.execute("DELETE FROM possible_answers WHERE question_id = ?", (question_id,))
        if question_data.possibleAnswers:
            answers_to_insert = [
                (answer.text, 1 if answer.is_correct else 0, question_id) 
                for answer in question_data.possibleAnswers
            ]
            cursor.executemany(
                "INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)",
                answers_to_insert
            )
        conn.commit()
        return 1 # Succès
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour: {e}")
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
    """Supprime une question et décale les autres."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        position = _get_question_position(cursor, question_id)
        if position is None:
            return 0

        cursor.execute("DELETE FROM possible_answers WHERE question_id = ?", (question_id,))
        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        
        # On décale les questions suivantes pour combler le trou
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