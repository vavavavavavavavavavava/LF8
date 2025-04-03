import requests
import mysql.connector
from PIL import Image, ImageTk
import io
import os

# MySQL-Verbindungsdaten
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'pokemon_db'
}

# Verbindung zur MySQL-Datenbank herstellen
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Funktion, um das Bild zu schwarz zu konvertieren
def convert_to_black(image):
    image = image.convert('RGBA')
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # Wenn der Pixel nicht transparent ist
                pixels[x, y] = (0, 0, 0, 255)  # Setze den Pixel auf schwarz
    return image

# Die Basis-URL der PokeAPI
url = "https://pokeapi.co/api/v2/pokemon?limit=1025"  # limit gibt an, wie viele Pokémon du auf einmal bekommst

# Ordner zum Speichern der Bilder erstellen (optional)
save_folder = 'pokemon_sprites'
os.makedirs(save_folder, exist_ok=True)

# Die Anfrage an die PokeAPI senden
response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    data = response.json()  # Antwort in ein Python-Dictionary umwandeln
    
    # Für jedes Pokémon die Daten herunterladen und speichern
    for pokemon in data['results']:
        pokemon_url = pokemon['url']
        
        # Detailanfrage für das Pokémon senden
        pokemon_details = requests.get(pokemon_url).json()
        
        # Pokémon-Name und Pokédex-Nr
        pokemon_name = pokemon_details['name']
        pokemon_id = pokemon_details['id']
        
        # Das Front-Artwork des Pokémon
        front_sprite_url = pokemon_details['sprites']['other']['official-artwork']['front_default']
        
        if front_sprite_url:
            # Originalbild herunterladen
            img_response = requests.get(front_sprite_url)
            
            if img_response.status_code == 200:
                original_image = Image.open(io.BytesIO(img_response.content))
                
                # Bild zu schwarz konvertieren
                black_image = convert_to_black(original_image)
                
                # Das originale Bild und das konvertierte Bild als BLOB speichern
                original_image_blob = io.BytesIO()
                original_image.save(original_image_blob, format='PNG')
                original_image_blob.seek(0)  # Setze den Pointer zurück
                
                black_image_blob = io.BytesIO()
                black_image.save(black_image_blob, format='PNG')
                black_image_blob.seek(0)
                
                # Pokémon-Daten in die MySQL-Datenbank speichern (Insert Ignore um Duplikate zu vermeiden)
                cursor.execute('''
                INSERT IGNORE INTO pokemon (pokedex_number, name, original_image, black_image)
                VALUES (%s, %s, %s, %s)
                ''', (pokemon_id, pokemon_name, original_image_blob.read(), black_image_blob.read()))
                
                # Speichern der Änderungen in der Datenbank
                conn.commit()
                
                print(f"Gespeichert: {pokemon_name} ({pokemon_id})")
            else:
                print(f"Fehler beim Herunterladen des Sprites für {pokemon_name}")
        else:
            print(f"Kein Front-Sprite für {pokemon_name}")

else:
    print("Fehler bei der Anfrage zur PokeAPI")

# Verbindung zur Datenbank schließen
conn.close()
