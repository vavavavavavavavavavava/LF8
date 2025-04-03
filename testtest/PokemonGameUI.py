import tkinter as tk
from PIL import ImageTk, Image
import random


class PokemonGameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Who's that Pokemon?")
        self.root.state('zoomed')

        # UI-Elemente initialisieren
        self.logo_label = None
        self.img_label = None
        self.answer_buttons = []
        self.start_button = None
        self.exit_button = None
        self.question_label = None
        self.next_button = None
        self.scoreboard_placeholder = None

        self.prepare_ui()

    def prepare_ui(self):
        # Logo laden und anzeigen
        logo_img = Image.open("logo.png")  # Dein Logo hier
        logo_img = logo_img.resize((265, 197))  # Größe des Logos anpassen
        logo_photo = ImageTk.PhotoImage(logo_img)

        # Logo-Label erstellen
        self.logo_label = tk.Label(self.root, image=logo_photo)
        self.logo_label.image = logo_photo  # Referenz zum Bild behalten

        # UI-Elemente erstellen
        self.start_button = tk.Button(self.root, text="Spiel Starten", command=self.start_game, width=15, height=2)
        self.exit_button = tk.Button(self.root, text="Beenden", command=self.exit_game, width=15, height=2)
        self.img_label = tk.Label(self.root)  # Bildplatzhalter
        self.question_label = tk.Label(self.root, text="")  # Frage-Platzhalter
        self.answer_buttons = [tk.Button(self.root, text="", width=15, height=2) for _ in range(4)]  # Antwortknöpfe
        self.scoreboard_placeholder = tk.Label(self.root, text="Scoreboard Placeholder", font=("Arial", 14))

        # Anfangs-Buttons platzieren
        self.logo_label.pack(pady=20)
        self.start_button.pack(pady=20)
        self.exit_button.pack(pady=5)
        self.scoreboard_placeholder.pack(pady=20)  # Scoreboard unter den Buttons platzieren (splash screen)

    def load_image(self, img):
        img = ImageTk.PhotoImage(img)  # PIL.Image zu PhotoImage konvertieren
        self.img_label.config(image=img)
        self.img_label.image = img  # Referenz behalten
        self.img_label.pack(pady=10)

    def check_answer(self, choice, button):
        # Alle Antwort-Buttons deaktivieren
        for btn in self.answer_buttons:
            btn.config(state="disabled", disabledforeground="black")  # Deaktiviert alle Knöpfe und setzt die Textfarbe auf schwarz

        if choice == self.game.get_correct_answer():
            button.config(bg="green", fg="black")  # Richtige Antwort wird grün, Text wird schwarz
        else:
            button.config(bg="red", fg="black")  # Falsche Antwort wird rot, Text wird schwarz

        # Sicherstellen, dass der richtige Antwort-Knopf grün wird
        for btn in self.answer_buttons:
            if btn.cget("text") == self.game.get_correct_answer():
                btn.config(bg="green", fg="black")  # Text wird schwarz und der Knopf wird grün

        # Das Originalbild anzeigen
        self.load_image(self.game.get_original_image())

        # Weiter-Button anzeigen
        self.next_button.pack(pady=20)

    def next_question(self):
        # Weiter-Button ausblenden und neue Frage laden
        self.next_button.pack_forget()
        self.ask_question(random.randint(1, 151))  # Nächste Frage, ersetze mit der nächsten Bildnummer
        # Antwortknöpfe zurücksetzen
        for btn in self.answer_buttons:
            btn.config(state="normal", bg="SystemButtonFace")

    def ask_question(self, pokedexNR):
        self.game.prepare_question_data(pokedexNR)
        # Anfangsbild und Frage anzeigen
        self.load_image(self.game.get_black_image())

        # Antwortknöpfe anzeigen
        for i, choice in enumerate(self.game.get_choices()):
            self.answer_buttons[i].config(text=choice, command=lambda c=choice, b=self.answer_buttons[i]: self.check_answer(c, b))
            self.answer_buttons[i].pack(pady=5)

        # Weiter-Button erstellen (wird sichtbar, wenn eine Antwort ausgewählt wurde)
        self.next_button = tk.Button(self.root, text="Weiter", command=self.next_question, width=15, height=2)

    def start_game(self):
        # Start- und Exit-Buttons ausblenden
        self.start_button.pack_forget()
        self.exit_button.pack_forget()

        # Layout anpassen
        self.logo_label.pack_forget()
        self.logo_label.pack(side="left", padx=20, pady=20)

        # Scoreboard on the right side during the game
        self.scoreboard_placeholder.pack(side="right", padx=20, pady=20)

        # Ask the first question
        self.ask_question(random.randint(1, 151))

    def exit_game(self):
        self.root.destroy()  # Fenster schließen
