import random
import getData

selected_pokemon_ids = set()

def random_exclude(pokedexNR):
    x = random.randint(1, 151)
    if x == pokedexNR:
        return random_exclude(pokedexNR)
    else:
        return getData.get_pokemon_name(x)
    
def display_pokemon_info(pokemon_id):
    """
    Fetches and displays Pokémon details.
    """
    name = getData.get_pokemon_name(pokemon_id)
    print(f"Name: {name}")

def test(pokedexNr):
    correct_answer = getData.get_pokemon_name(pokedexNr)
    choices = [random_exclude(pokedexNr),random_exclude(pokedexNr),random_exclude(pokedexNr),correct_answer]
    return choices

liste = test(1)
print(liste)
random.shuffle(liste)
print(liste)

