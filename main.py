# main.py
import tkinter as tk
from PokemonGame import PokemonGame
from PokemonGameUI import PokemonGameUI
from database_manager import PokemonDatabaseManager

class Main:
    def __init__(self):
        # Hauptfenster erstellen
        self.root = tk.Tk()

        # Instanz des Database Managers erstellen
        self.db_manager = PokemonDatabaseManager()

        # Game- und UI-Instanzen erstellen, Database Manager weitergeben
        self.game = PokemonGame(self.db_manager)
        self.game_ui = PokemonGameUI(self.root, self.game)

    def run(self):
        # Tkinter-Schleife ausführen
        self.root.mainloop()

    def check_database(self):
        print("Checking database...")
        if self.db_manager.get_highest_pokedex_number() < 1025:
            self.db_manager.fill_database()
        else:
            print("Database is already filled with Pokémon data.")
            
if __name__ == "__main__":
    app = Main()
    app.check_database()
    app.run()
