"""
The question module defines the `Question` class, which represents a Pokémon quiz question.
It retrieves Pokémon data such as names and images and generates multiple-choice answers.
"""

import random

class Question:
    """
    Represents a Pokémon quiz question.

    Attributes:
        pokedex_number (int): The Pokédex number of the Pokémon.
        correct_answer (str): The correct name of the Pokémon.
        original_image (PIL.Image): The original Pokémon image.
        black_image (PIL.Image): The blacked-out Pokémon image.
        choices (list): A list of answer choices, including the correct answer.
        mode (tuple): A tuple defining the range of Pokédex numbers to use (min, max).
    """

    def __init__(self, db_manager, mode=None):
        """
        Initializes a Question instance.

        Args:
            db_manager (PokemonDatabaseManager): The database manager instance.
            mode (tuple, optional): A tuple defining the range of Pokédex numbers (min, max).
                                    If None, the full range is used.
        """
        self.db_manager = db_manager
        self.mode = mode or (1, self.db_manager.max_pokedex_number)
        self.pokedex_number = random.randint(self.mode[0], self.mode[1])
        self.correct_answer = self.db_manager.get_pokemon_name(self.pokedex_number)
        self.original_image = self.db_manager.get_pokemon_image(self.pokedex_number)
        self.black_image = self.db_manager.get_black_image(self.pokedex_number)
        self.choices = self.generate_choices()

    def generate_choices(self):
        """
        Generates a list of answer choices, including the correct answer.

        Returns:
            list: A shuffled list of four Pokémon names, one of which is the correct answer.
        """
        choices = [self.correct_answer]
        while len(choices) < 4:
            choice = self.db_manager.get_pokemon_name(
                random.randint(self.mode[0], self.mode[1])
            )
            if choice and choice not in choices:
                choices.append(choice)
        random.shuffle(choices)
        return choices

    def get_correct_answer(self):
        """
        Retrieves the correct answer for the question.

        Returns:
            str: The correct Pokémon name.
        """
        return self.correct_answer

    def get_choices(self):
        """
        Retrieves the list of answer choices.

        Returns:
            list: A list of Pokémon names.
        """
        return self.choices

    def get_black_image(self):
        """
        Retrieves the blacked-out image of the Pokémon.

        Returns:
            PIL.Image: The blacked-out Pokémon image.
        """
        return self.black_image

    def get_original_image(self):
        """
        Retrieves the original image of the Pokémon.

        Returns:
            PIL.Image: The original Pokémon image.
        """
        return self.original_image
