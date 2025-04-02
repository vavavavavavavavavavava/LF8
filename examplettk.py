import tkinter as tk
from PIL import ImageTk  # Install Pillow if not already installed: pip install pillow
import getData
import random

# Funktion zum Laden und Anzeigen eines neuen Bildes
def load_black_image(pokedexNR):
    img = getData.get_black_image(pokedexNR)
    img = ImageTk.PhotoImage(img)  # PIL.Image zu PhotoImage konvertieren
    img_label.config(image=img)
    img_label.image = img  # Referenz behalten
    img_label.pack(pady=10)

def load_original_image(pokedexNR):
    img = getData.get_pokemon_image(pokedexNR)
    img = ImageTk.PhotoImage(img)  # PIL.Image zu PhotoImage konvertieren
    img_label.config(image=img)
    img_label.image = img  # Referenz behalten
    img_label.pack(pady=10)

def load_image(img):
    img = ImageTk.PhotoImage(img)  # PIL.Image zu PhotoImage konvertieren
    img_label.config(image=img)
    img_label.image = img  # Referenz behalten
    img_label.pack(pady=10)

def random_exclude(pokedexNR):
    x = random.randint(1, 151)
    if x == pokedexNR:
        return random_exclude(pokedexNR)
    else:
        return getData.get_pokemon_name(x)

def prepare_questionData(pokedexNr):
    #original_image = load_original_image(pokedexNr)
    original_image = getData.get_pokemon_image(pokedexNr)
    #black_image = load_black_image(pokedexNr)
    black_image = getData.get_black_image(pokedexNr)
    correct_answer = getData.get_pokemon_name(pokedexNr)
    choices = [random_exclude(pokedexNr),random_exclude(pokedexNr),random_exclude(pokedexNr),correct_answer]
    random.shuffle(choices)
    return correct_answer, choices, black_image, original_image
    

def question(pokedexNR):

    correct_answer,  choices, black_image, original_image = prepare_questionData(pokedexNR)
    # Anfangsbild und Frage anzeigen
    #load_black_image(pokedexNR)  # Anfangsbild, ersetze mit deinem Bildpfad
    load_image(black_image)
    question_label.config(text="Welches Pokémon ist das?")
    question_label.pack()

    # Mögliche Antworten
    #correct_answer = getData.get_pokemon_name(pokedexNR)
    #choices = [random_exclude(pokedexNR),random_exclude(pokedexNR),random_exclude(pokedexNR), correct_answer]

    # Funktion zur Überprüfung der Antwort
    def check_answer(choice, button):
        # Alle Antwort-Buttons deaktivieren
        for btn in answer_buttons:
            btn.config(state="disabled")  # Deaktiviert alle Knöpfe

        if choice == correct_answer:
            button.config(bg="green")  # Richtige Antwort wird grün
        else:
            button.config(bg="red")  # Falsche Antwort wird rot

        # Sicherstellen, dass der richtige Antwort-Knopf grün wird
        for btn in answer_buttons:
            if btn.cget("text") == correct_answer:
                btn.config(bg="green")

        #load_original_image(pokedexNR)
        load_image(original_image)

        # Weiter-Button anzeigen
        next_button.pack(pady=20)

    # Funktion zum Weitergehen zur nächsten Frage
    def next_question():
        # Weiter-Button ausblenden und neue Frage laden
        next_button.pack_forget()
        question(random.randint(1,151))  # Nächste Frage, ersetze mit der nächsten Bildnummer
        # Antwortknöpfe zurücksetzen
        for btn in answer_buttons:
            btn.config(state="normal", bg="SystemButtonFace")

    # Antwortknöpfe anzeigen
    for i, choice in enumerate(choices):
        answer_buttons[i].config(text=choice, command=lambda c=choice, b=answer_buttons[i]: check_answer(c, b))
        answer_buttons[i].pack(pady=5)

    # Weiter-Button erstellen (wird sichtbar, wenn eine Antwort ausgewählt wurde)
    next_button = tk.Button(root, text="Weiter", command=next_question, width=15, height=2)

# Funktion zum Starten des Spiels
def start_game():
    # Start- und Exit-Buttons ausblenden
    start_button.pack_forget()
    exit_button.pack_forget()
    question(random.randint(1,151))



# Funktion zum Beenden des Spiels
def exit_game():
    root.destroy()  # Fenster schließen

# Hauptfenster erstellen
root = tk.Tk()
root.title("Quiz Spiel")
root.geometry("800x800")

# UI-Elemente erstellen
start_button = tk.Button(root, text="Spiel Starten", command=start_game, width=15, height=2)
exit_button = tk.Button(root, text="Beenden", command=exit_game, width=15, height=2)
img_label = tk.Label(root)  # Bildplatzhalter
question_label = tk.Label(root, text="")  # Frage-Platzhalter
answer_buttons = [tk.Button(root, text="", width=15, height=2) for _ in range(4)]  # Antwortknöpfe

# Anfangs-Buttons platzieren
start_button.pack(pady=20)
exit_button.pack()

# Tkinter-Schleife ausführen
root.mainloop()
