"""
This module defines the Score class, which is used to manage and track a score value.
"""

class Score:
    """
    A class to represent and manage a score.
    """

    def __init__(self):
        """
        Initialize the Score object with a score value of 0.
        """
        self.score = 0

    def increase(self):
        """
        Increment the score by 1.
        """
        self.score += 1

    def get(self):
        """
        Retrieve the current score value.

        Returns:
            int: The current score.
        """
        return self.score
