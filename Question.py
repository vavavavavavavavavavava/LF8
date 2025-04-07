import random
import getData

class Question:
    def __init__(self, pokedexNr):
        self.pokedexNr = pokedexNr
        self.correct_answer = getData.get_pokemon_name(pokedexNr)
        self.original_image = getData.get_pokemon_image(pokedexNr)
        self.black_image = getData.get_black_image(pokedexNr)
        self.choices = self.generate_choices()

    def generate_choices(self):
        """Erstellt eine Liste mit Antwortmöglichkeiten, einschließlich der richtigen Antwort."""
        choices = [self.correct_answer]
        while len(choices) < 4:
            choice = getData.get_pokemon_name(random.randint(1, 1025))
            if choice and choice not in choices:
                choices.append(choice)
        random.shuffle(choices)
        return choices

    def get_correct_answer(self):
        return self.correct_answer

    def get_choices(self):
        return self.choices

    def get_black_image(self):
        return self.black_image

    def get_original_image(self):
        return self.original_image