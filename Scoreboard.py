"""
Scoreboard Module

This module provides a `Scoreboard` class to interact with a database of highscores.
It allows retrieving and submitting highscores using the `getData` module.
"""

import getData

class Scoreboard:
    """
    A class to manage highscores.

    This class provides methods to retrieve and submit highscores
    to a database using the `getData` module.
    """

    def __init__(self):
        """
        Initializes the Scoreboard instance.
        """
        pass

    def get_highscores(self):
        """
        Retrieves the highscores from the database.

        Returns:
            list: A list of highscores retrieved from the database.
        """
        return getData.get_highscore()

    def submit_highscore(self, name, score):
        """
        Submits a new highscore to the database.

        Args:
            name (str): The name of the player.
            score (int): The score achieved by the player.
        """
        getData.set_highscore(name, score)
