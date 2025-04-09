"""
This module provides functionality to manage a Pokémon database. It includes methods to fetch
Pokémon data from the PokeAPI, process and store the data in a MySQL database, and retrieve Pokémon
information such as names, images, and highscores.
"""

import io
import time
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import requests
import mysql.connector
from PIL import Image

class PokemonDatabaseManager:
    """
    A class to manage Pokémon data in a MySQL database. It provides methods to fetch data from the
    PokeAPI, process and store the data, and retrieve Pokémon information and highscores.
    """

    def __init__(self, max_pokedex_number=1025):
        """
        Initializes the PokemonDatabaseManager with database configuration and API URL.

        Args:
            max_pokedex_number (int): The maximum Pokédex number to fetch from the PokeAPI.
        """
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'passwort',
            'database': 'pokemon_db'
        }
        self.max_pokedex_number = max_pokedex_number
        self.api_url = f"https://pokeapi.co/api/v2/pokemon?limit={self.max_pokedex_number}"

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
        response = requests.get(self.api_url, timeout=10)
        if response.status_code == 200:
            return response.json()
        print("Error while requesting data from the PokeAPI")
        return None

    def fetch_pokemon_details(self, pokemon_url):
        """
        Fetches detailed data for a specific Pokémon from the PokeAPI.

        Args:
            pokemon_url (str): The URL to fetch the Pokémon details.

        Returns:
            dict: The JSON response containing Pokémon details, or None if the request fails.
        """
        response = requests.get(pokemon_url, timeout=10)
        if response.status_code == 200:
            return response.json()
        print(f"Error while fetching details from {pokemon_url}")
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
                a = pixels[x, y][3]
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
            tuple: A tuple containing Pokémon ID, name, original image blob, and black image blob,
                   or None if processing fails.
        """
        pokemon_details = self.fetch_pokemon_details(pokemon['url'])
        if not pokemon_details:
            return None

        pokemon_name = pokemon_details['name']
        pokemon_id = pokemon_details['id']
        front_sprite_url = pokemon_details['sprites']['other']['official-artwork']['front_default']

        print(f"Fetching Pokémon: {pokemon_name} (ID: {pokemon_id})")

        if front_sprite_url:
            img_response = requests.get(front_sprite_url, timeout=10)
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

                return (
                    pokemon_id, pokemon_name, original_image_blob.read(), black_image_blob.read())
        return None

    def process_pokemon_data_parallel(self, data, cursor):
        """
        Processes Pokémon data in parallel and saves it to the database.

        Args:
            data (dict): The Pokémon data fetched from the PokeAPI.
            cursor (mysql.connector.cursor.MySQLCursor): The database cursor.
        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            pokemon_batch = list(executor.map(self.fetch_and_process_pokemon, data['results']))

        # Filter out None values
        pokemon_batch = [p for p in pokemon_batch if p]

        # Batch insert into the database
        self.save_pokemon_batch_to_database(cursor, pokemon_batch)
        print(f"{len(pokemon_batch)} Pokémon records saved.")

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
        cursor.execute(
            'SELECT original_image FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
        result = cursor.fetchone()
        conn.close()

        if result and result['original_image']:
            image_data = result['original_image']
            image = Image.open(BytesIO(image_data))
            return image
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
        cursor.execute(
            'SELECT black_image FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
        result = cursor.fetchone()
        conn.close()

        if result and result['black_image']:
            image_data = result['black_image']
            image = Image.open(BytesIO(image_data))
            return image
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

        Checks if the database is already filled. If not, fetches data from the PokeAPI,
        processes it, and stores it in the database.
        """
        print("Checking database...")
        if self.get_highest_pokedex_number() >= self.max_pokedex_number:
            print("Database is already filled with Pokémon data.")
            return

        print("Filling database with Pokémon data...")
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
        print(f"Database population completed. Duration: {elapsed_time:.2f} seconds")

    def get_highest_pokedex_number(self):
        """
        Retrieves the highest Pokédex number from the database.

        Returns:
            int: The highest Pokédex number, or None if the table is empty.
        """
        conn = self.connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT MAX(pokedex_number) AS highest_pokedex_number FROM pokemon')
        result = cursor.fetchone()
        conn.close()

        if result and result['highest_pokedex_number'] is not None:
            return int(result['highest_pokedex_number'])
        return 0
