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
        self.root.mainloop()

    def prepare(self):
        """
        Prepares the game by filling the database and starting a new game.
        This method is called before starting the main game loop.
        """
        self.db_manager.fill_database()
        print("Starting game...")
        self.game.start_new_game()
        self.game_ui.prepare_ui()

if __name__ == "__main__":
    print("Starting Pokémon Game...")
    app = Main()
    app.prepare()
    app.run()
