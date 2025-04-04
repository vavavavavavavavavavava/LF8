# game.py
import random
import getData

class PokemonGame:
    def __init__(self):
        self.correct_answer = None
        self.choices = None
        self.black_image = None
        self.original_image = None
        self.score = 0
        self.correct = True

    def random_exclude(self, pokedexNR):
        x = random.randint(1, 1025)
        if x == pokedexNR:
            return self.random_exclude(pokedexNR)
        else:
            return getData.get_pokemon_name(x)

    def prepare_question_data(self, pokedexNr):
        # Werte für die Frage generieren und als Instanzvariablen speichern
        self.original_image = getData.get_pokemon_image(pokedexNr)
        self.black_image = getData.get_black_image(pokedexNr)
        self.correct_answer = getData.get_pokemon_name(pokedexNr)
        self.choices = [self.random_exclude(pokedexNr), self.random_exclude(pokedexNr), self.random_exclude(pokedexNr), self.correct_answer]
        random.shuffle(self.choices)

    def get_correct_answer(self):
        return self.correct_answer

    def get_choices(self):
        return self.choices

    def get_black_image(self):
        return self.black_image

    def get_original_image(self):
        return self.original_image
    
    def reset_score(self):
        self.score = 0

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def reset_correct(self):
        self.correct = True

    def wrong_answer(self):
        self.correct = False
    
    def get_correct(self):
        return self.correct

    def get_highscores(self):
        return getData.get_highscore()

    def submit_highscore(self, name):
        getData.set_highscore(name, self.score)