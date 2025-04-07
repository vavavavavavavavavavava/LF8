"""
PokemonGameUI Module

This module provides a graphical user interface (GUI) for the "Who's that Pokemon?" game.
It uses the tkinter library for UI components and integrates with the game logic.
"""

import tkinter as tk
from PIL import ImageTk, Image


class PokemonGameUI:
    """
    A class to represent the GUI for the "Who's that Pokemon?" game.

    Attributes:
        root (tk.Tk): The root window of the tkinter application.
        game (object): The game logic object to interact with.
    """

    def __init__(self, root, game):
        """
        Initialize the PokemonGameUI class.

        Args:
            root (tk.Tk): The root window of the tkinter application.
            game (object): The game logic object to interact with.
        """
        self.root = root
        self.game = game
        self.root.title("Who's that Pokemon?")
        self.root.state('zoomed')

        # Initialize UI elements
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
        """
        Prepare the UI elements for the main menu and start view.
        """
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=2, uniform="equal")
        self.root.grid_columnconfigure(2, weight=1, uniform="equal")

        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((397, 295))
        logo_photo = ImageTk.PhotoImage(logo_img)

        self.logo_label = tk.Label(self.root, image=logo_photo)
        self.logo_label.image = logo_photo

        self.start_button = tk.Button(
            self.root, text="Start Game", command=self.start_game, width=15, height=2
        )
        self.scoreboard_button = tk.Button(
            self.root, text="Scoreboard", command=self.scoreboard, width=15, height=2
        )
        self.exit_button = tk.Button(
            self.root, text="Exit", command=self.exit_game, width=15, height=2
        )
        self.img_label = tk.Label(self.root)
        self.question_label = tk.Label(self.root, text="")
        self.answer_buttons = [
            tk.Button(self.root, text="", width=15, height=2) for _ in range(4)
        ]
        self.scoreboard_data = tk.Label(
            self.root, text=f"Score: {self.game.get_score()}", font=("Arial", 14)
        )
        self.next_button = tk.Button(
            self.root, text="Continue", command=self.next_question, width=15, height=2
        )

        self.show_main_menu()

    def show_main_menu(self):
        """
        Create and display the main menu. The logo remains at the top.
        """
        self.logo_label.grid(row=0, column=1, pady=20, sticky="nsew")
        self.start_button.grid(row=1, column=1, pady=20, sticky="nsew")
        self.scoreboard_button.grid(row=2, column=1, pady=20, sticky="nsew")
        self.exit_button.grid(row=3, column=1, pady=20, sticky="nsew")

        self.scoreboard_data.grid_forget()
        self.next_button.grid_forget()

    def update_scoreboard(self):
        """
        Update the score displayed in the scoreboard.
        """
        self.scoreboard_data.config(text=f"Score: {self.game.get_score()}")

    def load_image(self, img):
        """
        Load and display an image in the UI.

        Args:
            img (PIL.Image): The image to display.
        """
        img = ImageTk.PhotoImage(img)
        self.img_label.config(image=img)
        self.img_label.image = img
        self.img_label.grid(row=0, column=1, pady=10)

    def check_answer(self, choice, button):
        """
        Check the player's answer and display the result.

        Args:
            choice (str): The player's selected answer.
            button (tk.Button): The button corresponding to the selected answer.
        """
        question = self.game.get_current_question()

        for btn in self.answer_buttons:
            btn.config(state="disabled", disabledforeground="black")

        if choice == question.get_correct_answer():
            button.config(bg="green", fg="black")
            self.game.increase_score()
            self.update_scoreboard()
        else:
            button.config(bg="red", fg="black")
            self.game.wrong_answer()

        for btn in self.answer_buttons:
            if btn.cget("text") == question.get_correct_answer():
                btn.config(bg="green", fg="black")

        self.load_image(question.get_original_image())
        self.next_button.grid(row=5, column=1, pady=20)

    def next_question(self):
        """
        Proceed to the next question.
        """
        self.next_button.grid_forget()

        for btn in self.answer_buttons:
            btn.config(state="normal", bg="SystemButtonFace")
            btn.grid_forget()

        if not self.game.get_correct():
            self.end_game()
        else:
            self.game.next_question()
            self.ask_question()

    def go_to_main_menu(self):
        """
        Return to the main menu and reset the game state.
        """
        for widget in self.root.winfo_children():
            widget.grid_forget()

        self.show_main_menu()
        self.game.reset_correct()

    def ask_question(self):
        """
        Display the current question and answer choices.
        """
        question = self.game.get_current_question()
        self.load_image(question.get_black_image())

        for i, choice in enumerate(question.get_choices()):
            self.answer_buttons[i].config(
                text=choice,
                command=lambda c=choice, b=self.answer_buttons[i]: self.check_answer(c, b)
            )
            self.answer_buttons[i].grid(row=i + 1, column=1, pady=5)

    def start_game(self):
        """
        Start a new game and display the first question.
        """
        self.game.start_new_game()

        self.start_button.grid_forget()
        self.scoreboard_button.grid_forget()
        self.exit_button.grid_forget()

        self.logo_label.grid(row=0, column=0, pady=20, padx=20)
        self.scoreboard_data.grid(row=0, column=2, pady=20, padx=20)

        self.ask_question()

    def scoreboard(self):
        """
        Display the scoreboard with high scores.
        """
        for widget in self.root.winfo_children():
            widget.grid_forget()

        self.logo_label.grid(row=0, column=1, pady=20)

        highscores = self.game.get_highscores()
        for i, entry in enumerate(highscores):
            name, score = entry['name'], entry['score']
            tk.Label(
                self.root, text=f"{i + 1}. {name}: {score}", font=("Arial", 14)
            ).grid(row=i + 1, column=1, pady=5)

        self.menu_button = tk.Button(
            self.root, text="Back", command=self.go_to_main_menu, font=("Arial", 14)
        )
        self.menu_button.grid(row=len(highscores) + 2, column=1, pady=20)

    def end_game(self):
        """
        End the game and display the player's score with an option to submit their name.
        """
        for widget in self.root.winfo_children():
            widget.grid_forget()

        self.logo_label.grid(row=0, column=1, pady=20)

        self.score_label = tk.Label(
            self.root, text=f"Your Score: {self.game.get_score()}", font=("Arial", 24, "bold")
        )
        self.score_label.grid(row=1, column=1, pady=10)

        self.name_label = tk.Label(self.root, text="Enter your name:", font=("Arial", 14))
        self.name_label.grid(row=2, column=1, pady=20)
        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.name_entry.grid(row=3, column=1, pady=20)

        self.submit_button = tk.Button(
            self.root, text="Submit", command=self.submit_name_and_go_to_menu, font=("Arial", 14)
        )
        self.submit_button.grid(row=4, column=1, pady=20)

        self.root.bind('<Return>', lambda event: self.submit_name_and_go_to_menu())
        self.game.reset_correct()

    def submit_name_and_go_to_menu(self):
        """
        Submit the player's name and return to the main menu.
        """
        player_name = self.name_entry.get().strip()[:20]

        if len(player_name) < 1:
            error_label = tk.Label(
                self.root, text="Please enter a valid name!", font=("Arial", 12), fg="red"
            )
            error_label.grid(row=5, column=1, pady=10)
            self.root.after(3000, error_label.destroy)
            return

        self.game.submit_highscore(player_name)
        self.update_scoreboard()
        self.go_to_main_menu()

    def exit_game(self):
        """
        Exit the game and close the application.
        """
        self.root.destroy()
