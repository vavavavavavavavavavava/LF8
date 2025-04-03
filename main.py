# main.py
import tkinter as tk
from PokemonGame import PokemonGame
from PokemonGameUI import PokemonGameUI

# Hauptfenster erstellen
root = tk.Tk()

# Game- und UI-Instanzen erstellen
game = PokemonGame()
game_ui = PokemonGameUI(root, game)

# Tkinter-Schleife ausführen
root.mainloop() 
