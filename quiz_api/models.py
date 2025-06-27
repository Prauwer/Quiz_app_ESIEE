import json

class PossibleAnswer():
    """Classe représentant une réponse possible à une question."""
    def __init__(self, text: str, is_correct: bool, id: int = None, question_id: int = None):
        self.id = id
        self.text = text
        self.is_correct = is_correct

class Question():
    """Classe représentant une question du quiz."""
    def __init__(self, position: int, title: str, text: str, image: str = None, id: int = None):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possibleAnswers = []

class Participation():
    """Classe représentant une participation au quiz."""
    def __init__(self, player_name: str, answers: list, score: int = 0, id: int = None):
        self.id = id
        self.player_name = player_name
        self.answers = answers # Liste des ID des réponses choisies
        self.score = score

    def to_json_summary(self, answers_summary):
        """Retourne un résumé de la participation pour la réponse de l'API."""
        return {
            "playerName": self.player_name,
            "score": self.score,
            "answersSummaries": answers_summary
        }