"""
This module serves as the entry point for the Pokémon game application. 
It initializes the main application window, manages the database, and starts the game UI.
"""

import tkinter as tk
from pokemon_game import PokemonGame
from pokemon_game_ui import PokemonGameUI
from database_manager import PokemonDatabaseManager

class Main:
    """
    The Main class initializes and runs the Pokémon game application.

    Attributes:
        root (tk.Tk): The main Tkinter window.
        db_manager (PokemonDatabaseManager): Manages the Pokémon database.
        game (PokemonGame): Handles the game logic.
        game_ui (PokemonGameUI): Manages the game user interface.
    """

    def __init__(self):
        """
        Initializes the main application by creating the main window, 
        database manager, game logic, and user interface.
        """
        # Hauptfenster erstellen
        self.root = tk.Tk()

        # Instanz des Database Managers erstellen
        self.db_manager = PokemonDatabaseManager()

        # Game- und UI-Instanzen erstellen, Database Manager weitergeben
        self.game = PokemonGame(self.db_manager)
        self.game_ui = PokemonGameUI(self.root, self.game)

    def run(self):
        """
        Starts the Tkinter main loop to run the application.
        """
        # Tkinter-Schleife ausführen
        self.root.mainloop()

    def check_database(self):
        """
        Checks if the Pokémon database is filled. If not, it populates the database.
        """
        print("Checking database...")
        if self.db_manager.get_highest_pokedex_number() < self.db_manager.max_pokedex_number:
            self.db_manager.fill_database()
        else:
            print("Database is already filled with Pokémon data.")

if __name__ == "__main__":
    print("Starting Pokémon Game...")
    app = Main()
    print("Initializing database...")
    app.check_database()
    print("Starting game...")
    app.game.start_new_game()
    app.game_ui.prepare_ui()
    app.run()
