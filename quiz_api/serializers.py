from models import Question, PossibleAnswer

def json_to_question(json_data):
    """Convertit un dictionnaire JSON en objet Question, incluant ses réponses."""
    question = Question(
        position=json_data.get('position'),
        title=json_data.get('title'),
        text=json_data.get('text'),
        image=json_data.get('image', None)
    )
    answers_data = json_data.get('possibleAnswers', [])
    for answer_data in answers_data:
        question.possibleAnswers.append(
            PossibleAnswer(
                text=answer_data.get('text'),
                is_correct=answer_data.get('isCorrect')
            )
        )
    return question

def question_to_json(question: Question):
    """Convertit un objet Question et ses réponses en dictionnaire JSON."""
    return {
        'id': question.id,
        'position': question.position,
        'title': question.title,
        'text': question.text,
        'image': question.image,
        'possibleAnswers': [
            {'text': answer.text, 'isCorrect': answer.is_correct} 
            for answer in question.possibleAnswers
        ]
    }

def db_row_to_question(row):
    """Convertit une ligne de la table questions (sqlite3.Row) en objet Question."""
    if not row:
        return None
    return Question(
        id=row['id'],
        position=row['position'],
        title=row['title'],
        text=row['text'],
        image=row['image']
    )

def db_row_to_answer(row):
    """Convertit une ligne de la table possible_answers (sqlite3.Row) en objet PossibleAnswer."""
    if not row:
        return None
    return PossibleAnswer(
        id=row['id'],
        text=row['text'],
        is_correct=bool(row['is_correct']), # Convertit l'entier (0/1) en booléen
        question_id=row['question_id']
    )