"""
Module: scoretest
This module contains unit tests for the Score class, which is responsible for 
managing a score value. The tests ensure that the Score class behaves as expected.
"""

import unittest
from score import Score

class TestScore(unittest.TestCase):
    """
    TestScore is a test case class for the Score class.
    It contains unit tests to verify the functionality of the Score class, 
    including initialization, score incrementing, and handling multiple increments.
    """

    def setUp(self):
        """
        Set up a new Score object before each test.
        """
        self.score = Score()

    def test_initial_score(self):
        """
        Test that the initial score is 0.
        """
        self.assertEqual(self.score.get(), 0)

    def test_increase_score(self):
        """
        Test that the score increases by 1 when the increase method is called.
        """
        self.score.increase()
        self.assertEqual(self.score.get(), 1)

    def test_multiple_increases(self):
        """
        Test that the score increases correctly after multiple calls to increase.
        """
        for _ in range(5):
            self.score.increase()
        self.assertEqual(self.score.get(), 4)

if __name__ == '__main__':
    unittest.main()
