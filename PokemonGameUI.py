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
        self.scoreboard_data = None
        self.scoreboard_button = None
        self.submit_button = None
        self.menu_button = None

        self.prepare_ui()

    def prepare_ui(self):
        """UI-Elemente für das Hauptmenü und die Startansicht initialisieren."""
        # Define a 3-column layout
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")  # Left column for logo
        self.root.grid_columnconfigure(1, weight=2, uniform="equal")  # Center column for content
        self.root.grid_columnconfigure(2, weight=1, uniform="equal")  # Right column for score

        # Logo laden und anzeigen
        logo_img = Image.open("logo.png")  # Dein Logo hier
        logo_img = logo_img.resize((397, 295))  # Größe des Logos anpassen
        logo_photo = ImageTk.PhotoImage(logo_img)

        # Logo-Label erstellen
        self.logo_label = tk.Label(self.root, image=logo_photo)
        self.logo_label.image = logo_photo  # Referenz zum Bild behalten

        # UI-Elemente erstellen
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, width=15, height=2)
        self.scoreboard_button = tk.Button(self.root, text="Scoreboard", command=self.scoreboard, width=15, height=2)
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_game, width=15, height=2)
        self.img_label = tk.Label(self.root)  # Bildplatzhalter
        self.question_label = tk.Label(self.root, text="")  # Frage-Platzhalter
        self.answer_buttons = [tk.Button(self.root, text="", width=15, height=2) for _ in range(4)]  # Antwortknöpfe
        self.scoreboard_data = tk.Label(self.root, text=f"Score: {self.game.get_score()}", font=("Arial", 14))
        self.next_button = tk.Button(self.root, text="Continue", command=self.next_question, width=15, height=2)

        # Hauptmenü anzeigen
        self.show_main_menu()

    def show_main_menu(self):
        """Hauptmenü erstellen und anzeigen. Das Logo bleibt oben."""
        # Logo im Hauptmenü in der mittleren Spalte (Column 1) anzeigen
        self.logo_label.grid(row=0, column=1, pady=20, sticky="nsew")

        # UI-Elemente für das Hauptmenü in der mittleren Spalte unter dem Logo anzeigen
        self.start_button.grid(row=1, column=1, pady=20, sticky="nsew")
        self.scoreboard_button.grid(row=2, column=1, pady=20, sticky="nsew")
        self.exit_button.grid(row=3, column=1, pady=20, sticky="nsew")

        # Das Scoreboard ausblenden, wenn das Hauptmenü angezeigt wird
        self.scoreboard_data.grid_forget()
        self.next_button.grid_forget()

    def update_scoreboard(self):
        """Aktualisiere den Score im Scoreboard."""
        self.scoreboard_data.config(text=f"Score: {self.game.get_score()}")

    def load_image(self, img):
        img = ImageTk.PhotoImage(img)  # PIL.Image zu PhotoImage konvertieren
        self.img_label.config(image=img)
        self.img_label.image = img  # Referenz behalten
        self.img_label.grid(row=0, column=1, pady=10)  # Display image in the center column

    def check_answer(self, choice, button):
            # Alle Antwort-Buttons deaktivieren
            for btn in self.answer_buttons:
                btn.config(state="disabled", disabledforeground="black")

            if choice == self.game.get_correct_answer():
                button.config(bg="green", fg="black")  # Richtige Antwort wird grün
                self.game.increase_score()
                self.update_scoreboard()
            else:
                button.config(bg="red", fg="black")  # Falsche Antwort wird rot
                self.game.wrong_answer()

            # Sicherstellen, dass der richtige Antwort-Knopf grün wird
            for btn in self.answer_buttons:
                if btn.cget("text") == self.game.get_correct_answer():
                    btn.config(bg="green", fg="black")

            # Das Originalbild anzeigen
            self.load_image(self.game.get_original_image())

            # Weiter-Button anzeigen
            self.next_button.grid(row=5, column=1, pady=20)

    def next_question(self):
        # Weiter-Button ausblenden
        self.next_button.grid_forget()
        
        # Antwortknöpfe zurücksetzen
        for btn in self.answer_buttons:
            btn.config(state="normal", bg="SystemButtonFace")
            btn.grid_forget()

        if self.game.get_correct() == False:
            self.end_game()
        else:
            self.ask_question(random.randint(1, 1025))
    def go_to_main_menu(self):
        # Alle Widgets aus dem Fenster entfernen (Clean Slate)
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Hauptmenü anzeigen
        self.show_main_menu()

        # Zähler zurücksetzen
        self.game.reset_correct()

    def ask_question(self, pokedexNR):
        self.game.prepare_question_data(pokedexNR)

        # Anfangsbild anzeigen
        self.load_image(self.game.get_black_image())

        # Antwortknöpfe anzeigen
        for i, choice in enumerate(self.game.get_choices()):
            self.answer_buttons[i].config(text=choice, 
                                        command=lambda c=choice, b=self.answer_buttons[i]: self.check_answer(c, b))
            self.answer_buttons[i].grid(row=i+1, column=1, pady=5)

    def start_game(self):
        # Start- und Exit-Buttons ausblenden
        self.start_button.grid_forget()
        self.scoreboard_button.grid_forget()
        self.exit_button.grid_forget()

        # Logo in der linken Spalte anzeigen
        self.logo_label.grid(row=0, column=0, pady=20, padx=20)

        # Scoreboard in der rechten Spalte anzeigen
        self.scoreboard_data.grid(row=0, column=2, pady=20, padx=20)

        # Erste Frage stellen
        self.ask_question(random.randint(1, 1025))

    def scoreboard(self):
        # Alle Widgets aus dem Fenster entfernen (Clean Slate)
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Logo in der mittleren Spalte anzeigen
        self.logo_label.grid(row=0, column=1, pady=20)

    def scoreboard(self):
        # Alle Widgets aus dem Fenster entfernen (Clean Slate)
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Logo in der mittleren Spalte anzeigen
        self.logo_label.grid(row=0, column=1, pady=20)

        # Highscores aus der Datenbank abrufen und anzeigen
        highscores = self.game.get_highscores()
        for i, entry in enumerate(highscores):
            name, score = entry['name'], entry['score']
            tk.Label(self.root, text=f"{i+1}. {name}: {score}", font=("Arial", 14)).grid(row=i+1, column=1, pady=5)

        # "Zurück"-Button unter der Highscore-Liste platzieren
        self.menu_button = tk.Button(self.root, text="Back", command=self.go_to_main_menu, font=("Arial", 14))
        self.menu_button.grid(row=len(highscores) + 2, column=1, pady=20)

        

    def end_game(self):
        # Alle Widgets aus dem Fenster entfernen (Clean Slate)
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Logo zurück an die Spitze der mittleren Spalte (Column 1)
        self.logo_label.grid(row=0, column=1, pady=20)

        # Score anzeigen
        self.score_label = tk.Label(self.root, text=f"Your Score: {self.game.get_score()}", font=("Arial", 24, "bold"))
        self.score_label.grid(row=1, column=1, pady=10)

        # Eingabefeld und Beschriftung für den Namen anzeigen
        self.name_label = tk.Label(self.root, text="Enter your name:", font=("Arial", 14))
        self.name_label.grid(row=2, column=1, pady=20)
        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.name_entry.grid(row=3, column=1, pady=20)

        # Submit-Button erstellen
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_name_and_go_to_menu, font=("Arial", 14))
        self.submit_button.grid(row=4, column=1, pady=20)

        # Enter-Taste für die Eingabe binden
        self.root.bind('<Return>', lambda event: self.submit_name_and_go_to_menu())

        # Zähler zurücksetzen
        self.game.reset_correct()

    def submit_name_and_go_to_menu(self):
        # Name aus dem Eingabefeld holen und auf 255 Zeichen begrenzen
        player_name = self.name_entry.get().strip()[:20]  # Remove leading/trailing whitespace and truncate to 255 characters

        # Überprüfen, ob der Name gültig ist (mindestens ein Buchstabe)
        if len(player_name) < 1:
            # Fehlermeldung anzeigen
            error_label = tk.Label(self.root, text="Please enter a valid name!", font=("Arial", 12), fg="red")
            error_label.grid(row=5, column=1, pady=10)

            # Entferne die Fehlermeldung nach 3 Sekunden
            self.root.after(3000, error_label.destroy)
            return

        # Highscore speichern
        self.game.submit_highscore(player_name)
        self.game.reset_score()
        self.update_scoreboard()

        # Zurück zum Hauptmenü
        self.go_to_main_menu()

    def exit_game(self):
        self.root.destroy()