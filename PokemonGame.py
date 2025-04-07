# game.py
import random
from Question import Question
from Score import Score
from Scoreboard import Scoreboard

class pokemon_game:
    def __init__(self):
        """
        Initializes a new instance of the pokemon_game class.
        Sets up the initial state of the game, including the scoreboard,
        score, and the first question.
        """
        self.current_question = None
        self.score = None
        self.correct = True
        self.scoreboard = Scoreboard()
        self.start_new_game()

    def start_new_game(self):
        """
        Starts a new game by resetting the score and setting the correct flag to True.
        Also generates the first question for the game.
        """
        self.score = Score()
        self.correct = True
        self.next_question()

    def next_question(self):
        """
        Generates a new question by selecting a random Pokémon from the Pokédex.
        The question is created using the Question class.
        """
        pokedex_number = random.randint(1, 1025)
        self.current_question = Question(pokedex_number)

    def get_current_question(self):
        """
        Returns the current question object.

        Returns:
            Question: The current question instance.
        """
        return self.current_question

    def increase_score(self):
        """
        Increases the player's score by calling the increase method of the Score class.
        """
        self.score.increase()

    def get_score(self):
        """
        Retrieves the current score.

        Returns:
            int: The current score value.
        """
        return self.score.get()

    def reset_correct(self):
        """
        Resets the correct flag to True, indicating the player has not answered incorrectly.
        """
        self.correct = True

    def wrong_answer(self):
        """
        Sets the correct flag to False, indicating the player has answered incorrectly.
        """
        self.correct = False

    def get_correct(self):
        """
        Retrieves the current state of the correct flag.

        Returns:
            bool: True if the player has not answered incorrectly, False otherwise.
        """
        return self.correct

    def get_highscores(self):
        """
        Retrieves the list of highscores from the Scoreboard class.

        Returns:
            list: A list of highscores.
        """
        return self.scoreboard.get_highscores()

    def submit_highscore(self, name):
        """
        Submits the player's highscore to the scoreboard.

        Args:
            name (str): The name of the player to associate with the highscore.
        """
        self.scoreboard.submit_highscore(name, self.score.get())
