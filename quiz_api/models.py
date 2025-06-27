class PossibleAnswer():
    """Classe représentant une réponse possible à une question."""
    def __init__(self, text: str, is_correct: bool, id: int = None, question_id: int = None):
        self.id = id
        self.text = text
        # En Python, on utilise le type booléen natif (True/False)
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