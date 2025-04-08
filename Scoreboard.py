"""
Scoreboard Module

This module provides a `Scoreboard` class to interact with a database of highscores.
It allows retrieving and submitting highscores using the `PokemonDatabaseManager` class.
"""

from database_manager import PokemonDatabaseManager

class Scoreboard:
    """
    A class to manage highscores.

    This class provides methods to retrieve and submit highscores
    to a database using the `PokemonDatabaseManager` class.
    """

    def __init__(self, db_manager):
        """
        Initializes the Scoreboard instance.

        Args:
            db_manager (PokemonDatabaseManager): The database manager instance.
        """
        self.db_manager = db_manager

    def get_highscores(self):
        """
        Retrieves the highscores from the database.

        Returns:
            list: A list of highscores retrieved from the database.
        """
        return self.db_manager.get_highscore()

    def submit_highscore(self, name, score):
        """
        Submits a new highscore to the database.

        Args:
            name (str): The name of the player.
            score (int): The score achieved by the player.
        """
        self.db_manager.set_highscore(name, score)
