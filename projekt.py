"""
This is a Test
"""
import requests
import os

# Ordner zum Speichern der Bilder erstellen (falls er noch nicht existiert)
save_folder = 'pokemon_sprites'
os.makedirs(save_folder, exist_ok=True)

# Die Basis-URL der PokeAPI
url = "https://pokeapi.co/api/v2/pokemon?limit=151"  # limit gibt an, wie viele Pokémon du auf einmal bekommst

# Die Anfrage an die PokeAPI senden
response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war (Status-Code 200)
if response.status_code == 200:
    data = response.json()  # Die Antwort in ein Python-Dictionary umwandeln
    
    # Für jedes Pokémon in den Ergebnissen den Namen und die Pokédex-Nummer ausgeben
    for pokemon in data['results']:
        # Jedes Pokémon-Objekt hat die URL zu seiner Detailseite
        pokemon_url = pokemon['url']
        
        # Detailanfrage für das Pokémon senden, um die Pokédex-Nummer zu erhalten
        pokemon_details = requests.get(pokemon_url).json()
        
        # Pokédex-Nummer (ID) und Name aus den Details extrahieren
        pokemon_name = pokemon_details['name']
        pokemon_id = pokemon_details['id']
        pokemon_image = pokemon_details['sprites']['other']['official-artwork']['front_default']
        
        # Ausgabe der Pokémon-Daten
        print(f"Pokémon Name: {pokemon_name}, Pokédex Nr: {pokemon_id}, Sprite: {pokemon_image}")
        
        if pokemon_image:
            # Bild herunterladen
            img_response = requests.get(pokemon_image)
            
            if img_response.status_code == 200:
                # Bild speichern
                img_filename = f"{pokemon_id}_{pokemon_name}.png"
                img_path = os.path.join(save_folder, img_filename)
                
                # Bild auf der Festplatte speichern
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                
                print(f"Gespeichert: {img_filename}")
            else:
                print(f"Fehler beim Herunterladen des Sprites für {pokemon_name}")
        else:
            print(f"Kein Front-Sprite für {pokemon_name}")
else:
    print("Fehler bei der Anfrage zur PokeAPI")
