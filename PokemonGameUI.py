# ui.py
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
        """UI-Elemente für das Hauptmenü und die Startansicht initialisieren."""
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
        self.scoreboard_placeholder = tk.Label(self.root, text=f"Score: {self.game.get_score()}", font=("Arial", 14))

        # Hauptmenü anzeigen
        self.show_main_menu()

    def show_main_menu(self):
        """Hauptmenü erstellen und anzeigen. Das Logo bleibt oben."""
        # Logo im Hauptmenü oben anzeigen
        self.logo_label.pack(side="top", pady=20)

        # UI-Elemente für das Hauptmenü unter dem Logo anzeigen
        self.start_button.pack(pady=20)
        self.exit_button.pack(pady=5)

        # Das Scoreboard ausblenden, wenn das Hauptmenü angezeigt wird
        self.scoreboard_placeholder.pack_forget()  # Entfernen des Scoreboards im Hauptmenü

    def update_scoreboard(self):
        """Aktualisiere den Score im Scoreboard."""
        self.scoreboard_placeholder.config(text=f"Score: {self.game.get_score()}")

    def load_image(self, img):
        img = ImageTk.PhotoImage(img)  # PIL.Image zu PhotoImage konvertieren
        self.img_label.config(image=img)
        self.img_label.image = img  # Referenz behalten
        self.img_label.pack(pady=10)

    def check_answer(self, choice, button):
        # Alle Antwort-Buttons deaktivieren
        for btn in self.answer_buttons:
            btn.config(state="disabled", disabledforeground="black")  # Deaktiviert alle Knöpfe

        if choice == self.game.get_correct_answer():
            button.config(bg="green", fg="black")  # Richtige Antwort wird grün
            self.game.increase_score()
            self.update_scoreboard()  # Punktestand aktualisieren
            print(self.game.get_score())
        else:
            button.config(bg="red", fg="black")  # Falsche Antwort wird rot

        # Sicherstellen, dass der richtige Antwort-Knopf grün wird
        for btn in self.answer_buttons:
            if btn.cget("text") == self.game.get_correct_answer():
                btn.config(bg="green", fg="black")

        # Das Originalbild anzeigen
        self.load_image(self.game.get_original_image())

        # Counter erhöhen
        self.game.increase_counter()
        print(f"Counter: {self.game.get_counter()}")  # Zum Debuggen anzeigen, wie der Counter steigt

        self.next_button.pack(pady=20)

    def next_question(self):
        # Weiter-Button ausblenden und neue Frage laden
        self.next_button.pack_forget()
        self.ask_question(random.randint(1, 1025))  # Nächste Frage, ersetze mit der nächsten Bildnummer
        # Antwortknöpfe zurücksetzen
        for btn in self.answer_buttons:
            btn.config(state="normal", bg="SystemButtonFace")

    def go_to_main_menu(self):
        # Alle UI-Elemente, die zur Frage gehören, ausblenden
        self.img_label.pack_forget()  # Bild ausblenden
        self.question_label.config(text="")  # Frage zurücksetzen
        for btn in self.answer_buttons:
            btn.pack_forget()  # Alle Antwort-Buttons ausblenden
        self.next_button.pack_forget()  # Weiter-Button ausblenden

        # Hauptmenü anzeigen
        self.show_main_menu()

        # Zähler zurücksetzen
        self.game.reset_counter()

    def ask_question(self, pokedexNR):
        self.game.prepare_question_data(pokedexNR)
        # Anfangsbild und Frage anzeigen
        self.load_image(self.game.get_black_image())

        # Antwortknöpfe anzeigen
        for i, choice in enumerate(self.game.get_choices()):
            self.answer_buttons[i].config(text=choice, command=lambda c=choice, b=self.answer_buttons[i]: self.check_answer(c, b))
            self.answer_buttons[i].pack(pady=5)

        if self.game.get_counter() >= 3:
            self.go_to_main_menu()
        else:
            # Weiter-Button erstellen (wird sichtbar, wenn eine Antwort ausgewählt wurde)
            self.next_button = tk.Button(self.root, text="Weiter", command=self.next_question, width=15, height=2)

    def start_game(self):
        # Start- und Exit-Buttons ausblenden
        self.start_button.pack_forget()
        self.exit_button.pack_forget()

        # Logo wird links positioniert während des Spiels
        self.logo_label.pack_forget()
        self.logo_label.pack(side="left", padx=20, pady=20)  # Logo bleibt links

        # Scoreboard auf der rechten Seite während des Spiels anzeigen
        self.scoreboard_placeholder.pack(side="right", padx=20, pady=20)

        # Erste Frage stellen
        self.ask_question(random.randint(1, 1025))

    def exit_game(self):
        self.root.destroy()  # Fenster schließen
