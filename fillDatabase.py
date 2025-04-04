import requests
import mysql.connector
from PIL import Image
import io
import time  # Import für den Timer
from concurrent.futures import ThreadPoolExecutor

# MySQL-Verbindungsdaten
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passwort',
    'database': 'pokemon_db'
}

def connect_to_database():
    """Stellt die Verbindung zur MySQL-Datenbank her."""
    return mysql.connector.connect(**db_config)

def fetch_pokemon_data(api_url):
    """Sendet eine Anfrage an die PokeAPI und gibt die Daten zurück."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Fehler bei der Anfrage zur PokeAPI")
        return None

def fetch_pokemon_details(pokemon_url):
    """Holt die Detaildaten eines Pokémon von der PokeAPI."""
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der Details von {pokemon_url}")
        return None

def convert_to_black(image):
    """Konvertiert ein Bild zu einer schwarzen Version."""
    image = image.convert('RGBA')
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # Wenn der Pixel nicht transparent ist
                pixels[x, y] = (0, 0, 0, 255)  # Setze den Pixel auf schwarz
    return image

def save_pokemon_batch_to_database(cursor, pokemon_data, batch_size=100):
    """Speichert mehrere Pokémon-Daten in der MySQL-Datenbank in kleineren Batches."""
    sql = '''
    INSERT IGNORE INTO pokemon (pokedex_number, name, original_image, black_image)
    VALUES (%s, %s, %s, %s)
    '''
    for i in range(0, len(pokemon_data), batch_size):
        batch = pokemon_data[i:i + batch_size]
        cursor.executemany(sql, batch)

def fetch_and_process_pokemon(pokemon, cursor):
    """Holt und verarbeitet die Daten eines einzelnen Pokémon."""
    pokemon_details = fetch_pokemon_details(pokemon['url'])
    if not pokemon_details:
        return None
    
    pokemon_name = pokemon_details['name']
    pokemon_id = pokemon_details['id']
    front_sprite_url = pokemon_details['sprites']['other']['official-artwork']['front_default']
    
    if front_sprite_url:
        img_response = requests.get(front_sprite_url)
        if img_response.status_code == 200:
            original_image = Image.open(io.BytesIO(img_response.content))
            
            # Originalbild als BLOB speichern
            original_image_blob = io.BytesIO()
            original_image.save(original_image_blob, format='PNG')
            original_image_blob.seek(0)
            
            # Schwarzes Bild erstellen und als BLOB speichern
            black_image = convert_to_black(original_image)
            black_image_blob = io.BytesIO()
            black_image.save(black_image_blob, format='PNG')
            black_image_blob.seek(0)
            
            return (pokemon_id, pokemon_name, original_image_blob.read(), black_image_blob.read())
    return None

def process_pokemon_data_parallel(data, cursor):
    """Verarbeitet die Pokémon-Daten parallel und speichert sie in der Datenbank."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        pokemon_batch = list(executor.map(lambda p: fetch_and_process_pokemon(p, cursor), data['results']))
    
    # Filtere None-Werte heraus
    pokemon_batch = [p for p in pokemon_batch if p]
    
    # Batch-Insert in die Datenbank
    save_pokemon_batch_to_database(cursor, pokemon_batch)
    print(f"{len(pokemon_batch)} Pokémon-Datensätze gespeichert.")

def main():
    """Hauptfunktion des Programms."""
    start_time = time.time()  # Startzeit erfassen
    
    conn = connect_to_database()
    cursor = conn.cursor()
    
    api_url = "https://pokeapi.co/api/v2/pokemon?limit=1025"
    data = fetch_pokemon_data(api_url)
    
    if data:
        process_pokemon_data_parallel(data, cursor)
        conn.commit()
    
    conn.close()
    
    end_time = time.time()  # Endzeit erfassen
    elapsed_time = end_time - start_time
    print(f"Datenbankbefüllung abgeschlossen. Dauer: {elapsed_time:.2f} Sekunden")

if __name__ == "__main__":
    main()