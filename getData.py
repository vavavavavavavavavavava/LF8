import mysql.connector
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

# MySQL-Verbindungsdaten
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passwort',
    'database': 'pokemon_db'
}

# Verbindung zur MySQL-Datenbank herstellen
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Funktion, um den Namen eines Pokémon anhand der Pokédex-Nummer zu bekommen
def get_pokemon_name(pokedex_number):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
    result = cursor.fetchone()
    conn.close()
    # Falls ein Ergebnis gefunden wurde, den ersten Buchstaben groß machen
    if result:
        return result['name'].capitalize()
    else:
        return None

# Funktion, um das Originalbild eines Pokémon als PIL-Image zu erhalten
def get_pokemon_image(pokedex_number):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT original_image FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
    result = cursor.fetchone()
    conn.close()
    
    if result and result['original_image']:
        # Bilddaten (BLOB) extrahieren und in ein Image-Objekt umwandeln
        image_data = result['original_image']
        image = Image.open(BytesIO(image_data))
        return image
    else:
        return None

# Funktion, um das Schwarze Bild eines Pokémon als PIL-Image zu erhalten
def get_black_image(pokedex_number):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT black_image FROM pokemon WHERE pokedex_number = %s', (pokedex_number,))
    result = cursor.fetchone()
    conn.close()
    
    if result and result['black_image']:
        # Bilddaten (BLOB) extrahieren und in ein Image-Objekt umwandeln
        image_data = result['black_image']
        image = Image.open(BytesIO(image_data))
        return image
    else:
        return None

# Funktion, um das Bild in einem Tkinter-Fenster anzuzeigen
def display_pokemon_image(image):
    if image is None:
        print("Kein Bild gefunden.")
        return
    
    # Tkinter Fenster erstellen
    root = tk.Tk()
    root.title("Pokemon Image")

    # Bild in Tkinter-kompatibles Format konvertieren
    tk_image = ImageTk.PhotoImage(image)

    # Label hinzufügen, das das Bild enthält
    label = tk.Label(root, image=tk_image)
    label.pack()

    # Fenster starten
    root.mainloop()

def test_display_image():
    # Beispiel-Pokédex-Nr (z.B. Bulbasaur mit Nr 1)
    pokedex_number = 17
    image = get_pokemon_image(pokedex_number)
    display_pokemon_image(image)

def set_highscore(name, score):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO highscores (name, score) VALUES (%s, %s)', (name, score))
    conn.commit()
    conn.close()

def get_highscore():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name, score FROM highscores ORDER BY score DESC LIMIT 10')
    result = cursor.fetchall()
    conn.close()
    return result


#set_highscore("Vahan", 10)
#set_highscore("Jonah", 13)
#set_highscore("Max", 7)
#set_highscore("Peter", 3)
#set_highscore("Julia", 17)