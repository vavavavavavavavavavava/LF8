"""
This module provides functionality to manage a Pokémon database. It includes methods to fetch Pokémon data
from the PokeAPI, process and store the data in a MySQL database, and retrieve Pokémon information such as
names, images, and highscores.
"""

import requests
import mysql.connector
from PIL import Image
import io
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

class PokemonDatabaseManager:
    """
    A class to manage Pokémon data in a MySQL database. It provides methods to fetch data from the PokeAPI,
    process and store the data, and retrieve Pokémon information and highscores.
    """

    def __init__(self):
        """
        Initializes the PokemonDatabaseManager with database configuration and API URL.
        """
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'passwort',
            'database': 'pokemon_db'
        }
        self.api_url = "https://pokeapi.co/api/v2/pokemon?limit=1025"

    def connect_to_database(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            mysql.connector.connection.MySQLConnection: A connection object to the database.
        """
        return mysql.connector.connect(**self.db_config)

    def fetch_pokemon_data(self):
        """
        Sends a request to the PokeAPI to fetch Pokémon data.

        Returns:
            dict: The JSON response containing Pokémon data, or None if the request fails.
        """
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Fehler bei der Anfrage zur PokeAPI")
            return None

    def fetch_pokemon_details(self, pokemon_url):
        """
        Fetches detailed data for a specific Pokémon from the PokeAPI.

        Args:
            pokemon_url (str): The URL to fetch the Pokémon details.

        Returns:
            dict: The JSON response containing Pokémon details, or None if the request fails.
        """
        response = requests.get(pokemon_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Fehler beim Abrufen der Details von {pokemon_url}")
            return None

    def convert_to_black(self, image):
        """
        Converts an image to a black version.

        Args:
            image (PIL.Image.Image): The original image.

        Returns:
            PIL.Image.Image: The black version of the image.
        """
        image = image.convert('RGBA')
        pixels = image.load()
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 0:  # If the pixel is not transparent
                    pixels[x, y] = (0, 0, 0, 255)  # Set the pixel to black
        return image

    def save_pokemon_batch_to_database(self, cursor, pokemon_data, batch_size=100):
        """
        Saves multiple Pokémon data entries to the MySQL database in smaller batches.

        Args:
            cursor (mysql.connector.cursor.MySQLCursor): The database cursor.
            pokemon_data (list): A list of Pokémon data tuples to be inserted.
            batch_size (int): The size of each batch for insertion.
        """
        sql = '''
        INSERT IGNORE INTO pokemon (pokedex_number, name, original_image, black_image)
        VALUES (%s, %s, %s, %s)
        '''
        for i in range(0, len(pokemon_data), batch_size):
            batch = pokemon_data[i:i + batch_size]
            cursor.executemany(sql, batch)

    def fetch_and_process_pokemon(self, pokemon):
        """
        Fetches and processes data for a single Pokémon.

        Args:
            pokemon (dict): A dictionary containing Pokémon data from the PokeAPI.

        Returns:
            tuple: A tuple containing Pokémon ID, name, original image blob, and black image blob, or None if processing fails.
        """
        pokemon_details = self.fetch_pokemon_details(pokemon['url'])
        if not pokemon_details:
            return None
        
        pokemon_name = pokemon_details['name']
        pokemon_id = pokemon_details['id']
        front_sprite_url = pokemon_details['sprites']['other']['official-artwork']['front_default']
        
        if front_sprite_url:
            img_response = requests.get(front_sprite_url)
            if img_response.status_code == 200:
                original_image = Image.open(io.BytesIO(img_response.content))
                
                # Save original image as BLOB
                original_image_blob = io.BytesIO()
                original_image.save(original_image_blob, format='PNG')
                original_image_blob.seek(0)
                
                # Create black image and save as BLOB
                black_image = self.convert_to_black(original_image)
                black_image_blob = io.BytesIO()
                black_image.save(black_image_blob, format='PNG')
                black_image_blob.seek(0)
                
                return (pokemon_id, pokemon_name, original_image_blob.read(), black_image_blob.read())
        return None

    def process_pokemon_data_parallel(self, data, cursor):
        """
        Processes Pokémon data in parallel and saves it to the database.

        Args:
            data (dict): The Pokémon data fetched from the PokeAPI.
            cursor (mysql.connector.cursor.MySQLCursor): The database cursor.
        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            pokemon_batch = list(executor.map(lambda p: self.fetch_and_process_pokemon(p), data['results']))
        
        # Filter out None values
        pokemon_batch = [p for p in pokemon_batch if p]
        
        # Batch insert into the database
        self.save_pokemon_batch_to_database(cursor, pokemon_batch)
        print(f"{len(pokemon_batch)} Pokémon-Datensätze gespeichert.")

    def get_pokemon_name(self, pokedex_number):
        """
        Retrieves the name of a Pokémon by its Pokédex number.

        Args:
            pokedex_number (int): The Pokédex number of the Pokémon.

        Returns:
            str: The name of the Pokémon, or None if not found.
        """
        conn = self.connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT name FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result['name'].capitalize()
        else:
            return None

    def get_pokemon_image(self, pokedex_number):
        """
        Retrieves the original image of a Pokémon as a PIL image.

        Args:
            pokedex_number (int): The Pokédex number of the Pokémon.

        Returns:
            PIL.Image.Image: The original image of the Pokémon, or None if not found.
        """
        conn = self.connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT original_image FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result['original_image']:
            image_data = result['original_image']
            image = Image.open(BytesIO(image_data))
            return image
        else:
            return None

    def get_black_image(self, pokedex_number):
        """
        Retrieves the black image of a Pokémon as a PIL image.

        Args:
            pokedex_number (int): The Pokédex number of the Pokémon.

        Returns:
            PIL.Image.Image: The black image of the Pokémon, or None if not found.
        """
        conn = self.connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT black_image FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result['black_image']:
            image_data = result['black_image']
            image = Image.open(BytesIO(image_data))
            return image
        else:
            return None

    def set_highscore(self, name, score):
        """
        Saves a highscore to the database.

        Args:
            name (str): The name of the player.
            score (int): The score of the player.
        """
        conn = self.connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO highscores (name, score) VALUES (%s, %s)', (name, score))
        conn.commit()
        conn.close()

    def get_highscore(self):
        """
        Retrieves the top 10 highscores from the database.

        Returns:
            list: A list of dictionaries containing player names and scores.
        """
        conn = self.connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT name, score FROM highscores ORDER BY score DESC LIMIT 10')
        result = cursor.fetchall()
        conn.close()
        return result

    def fill_database(self):
        """
        Main function to populate the database with Pokémon data.

        Fetches data from the PokeAPI, processes it, and stores it in the database.
        """
        start_time = time.time()
        
        conn = self.connect_to_database()
        cursor = conn.cursor()
        data = self.fetch_pokemon_data()
        
        if data:
            self.process_pokemon_data_parallel(data, cursor)
            conn.commit()
        
        conn.close()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Datenbankbefüllung abgeschlossen. Dauer: {elapsed_time:.2f} Sekunden")
