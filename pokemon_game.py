"""
pokemon_game Module

This module contains the implementation of the PokemonGame class, which manages
the core logic of a Pokémon-themed game. The game involves generating random
Pokémon questions, tracking the player's score, and maintaining a scoreboard
of highscores.
"""

from question import Question
from score import Score
from scoreboard import Scoreboard

class PokemonGame:
    """
    PokemonGame Class

    This class represents the main game logic for a Pokémon-themed game. It handles
    generating questions, tracking the player's score, and interacting with the
    scoreboard. The game allows players to answer questions, track their progress,
    and submit their highscores.
    """

    def __init__(self, db_manager):
        """
        Initializes a new instance of the PokemonGame class.
        Sets up the initial state of the game, including the scoreboard,
        score, and the first question.

        Args:
            db_manager (PokemonDatabaseManager): The database manager instance.
        """
        self.db_manager = db_manager
        self.max_pokedex_number = db_manager.max_pokedex_number
        self.current_question = None
        self.score = None
        self.correct = True
        self.scoreboard = Scoreboard(self.db_manager)
        self.mode = (1, self.max_pokedex_number)

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
        self.current_question = Question(self.db_manager, self.mode)

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

    def change_mode(self, new_mode):
        """
        Changes the game mode based on the provided string.

        Args:
            new_mode (str): The name of the mode to switch to.
        """
        mode_mapping = {
            "All Pokemon": (1, self.max_pokedex_number),
            "Generation 1": (1, min(151, self.max_pokedex_number)),
            "Generation 2": (152, min(251, self.max_pokedex_number)),
            "Generation 3": (252, min(386, self.max_pokedex_number)),
            "Generation 4": (387, min(493, self.max_pokedex_number)),
            "Generation 5": (494, min(649, self.max_pokedex_number)),
            "Generation 6": (650, min(721, self.max_pokedex_number)),
            "Generation 7": (722, min(809, self.max_pokedex_number)),
            "Generation 8": (810, min(905, self.max_pokedex_number)),
            "Generation 9": (906, self.max_pokedex_number),
        }

        if new_mode in mode_mapping:
            self.mode = mode_mapping[new_mode]
        else:
            raise ValueError(f"Invalid mode: {new_mode}")
