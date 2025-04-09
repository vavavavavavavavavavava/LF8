"""
Unit tests for the PokemonDatabaseManager class.

This module contains test cases to verify the functionality of the
PokemonDatabaseManager class, including methods for connecting to the database,
retrieving Pokémon data, and managing highscores.
"""

import unittest
from database_manager import PokemonDatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """
    Test suite for the PokemonDatabaseManager class.

    This class contains unit tests for various methods of the
    PokemonDatabaseManager class, ensuring correct functionality
    for database operations and Pokémon data retrieval.
    """

    def setUp(self):
        """
        Set up the test case by creating an instance of PokemonDatabaseManager.
        """
        self.db_manager = PokemonDatabaseManager(10)

    def test_connect(self):
        """
        Test the database connection.
        """
        self.assertTrue(self.db_manager.connect())

    def test_get_pokemon_name(self):
        """
        Test retrieving a Pokémon name by its Pokedex number.
        """
        pokemon_name = self.db_manager.get_pokemon_name(1)
        self.assertIsInstance(pokemon_name, str)

    def test_get_pokemon_image(self):
        """
        Test retrieving a Pokémon image by its Pokedex number.
        """
        pokemon_image = self.db_manager.get_pokemon_image(1)
        self.assertIsNotNone(pokemon_image)

    def test_get_black_image(self):
        """
        Test retrieving a blacked-out image of a Pokémon by its Pokedex number.
        """
        black_image = self.db_manager.get_black_image(1)
        self.assertIsNotNone(black_image)

    def test_get_highscore(self):
        """
        Test retrieving highscores from the database.
        """
        highscores = self.db_manager.get_highscore()
        self.assertIsInstance(highscores, list)

    def test_set_highscore(self):
        """
        Test setting a new highscore in the database.
        """
        result = self.db_manager.set_highscore("TestPlayer", 100)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()