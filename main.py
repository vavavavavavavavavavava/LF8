# main.py
import tkinter as tk
from PokemonGame import PokemonGame
from PokemonGameUI import PokemonGameUI

class Main:
    def __init__(self):
        # Hauptfenster erstellen
        self.root = tk.Tk()

        # Game- und UI-Instanzen erstellen
        self.game = PokemonGame()
        self.game_ui = PokemonGameUI(self.root, self.game)

    def run(self):
        # Tkinter-Schleife ausführen
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()