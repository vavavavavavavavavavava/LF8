# game.py
import random
from Question import Question
from Score import Score
from Scoreboard import Scoreboard
import getData

class PokemonGame:
    def __init__(self):
        self.current_question = None
        self.score = None
        self.correct = True
        self.scoreboard = Scoreboard()  # Scoreboard-Instanz
        self.start_new_game()

    def start_new_game(self):
        """Startet ein neues Spiel und erstellt eine neue Score-Instanz."""
        self.score = Score()
        self.correct = True
        self.next_question()

    def next_question(self):
        """Erstellt eine neue Frage."""
        pokedexNr = random.randint(1, 1025)
        self.current_question = Question(pokedexNr)

    def get_current_question(self):
        return self.current_question

    def increase_score(self):
        self.score.increase()

    def get_score(self):
        return self.score.get()

    def reset_correct(self):
        self.correct = True

    def wrong_answer(self):
        self.correct = False

    def get_correct(self):
        return self.correct

    def get_highscores(self):
        """Holt die Highscores über die Scoreboard-Klasse."""
        return self.scoreboard.get_highscores()

    def submit_highscore(self, name):
        """Speichert den Highscore über die Scoreboard-Klasse."""
        self.scoreboard.submit_highscore(name, self.score.get())