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

if __name__ == "__main__":
    app = Main()
    app.run()
