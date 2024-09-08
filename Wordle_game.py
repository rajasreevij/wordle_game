import tkinter as tk
import random
import pygame

class WordleGame:
    def _init_(self, master, target_word):
        self.master = master
        self.master.title("Wordle Game")
        self.master.attributes("-fullscreen", True)
        self.target_word = target_word
        self.attempts = 0
        self.max_attempts = 5
        self.image_path = r"C:\Users\91939\Pictures\WhatsApp Image 2023-08-05 at 12.41.00.png"
        self.background_image = tk.PhotoImage(file=self.image_path)
        self.background_image = self.background_image.subsample(2)  # Adjust the factor as needed

        # Create a Label to display the background image
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a label to display the target word
        self.target_label = tk.Label(master, text="----GUESS THE WORD----", font=("Helvetica", 24, "bold"))
        self.target_label.pack()

        # Create a grid to show attempts and feedback
        self.grid_frame = tk.Frame(master)
        self.grid_frame.pack()

        self.grid = []
        for i in range(self.max_attempts):
            row = []
            for j in range(len(self.target_word)):
                cell = tk.Label(self.grid_frame, text=" ", font=("Arial", 16), width=4, height=2, borderwidth=3,
                                relief="ridge", bg="light green")
                cell.grid(row=i, column=j, padx=10, pady=10)
                row.append(cell)
            self.grid.append(row)

        # Create an input entry field and a submit button
        self.input_entry = tk.Entry(master, font=("Arial", 16), width=20)
        self.input_entry.pack()
        self.submit_button = tk.Button(master, text="Submit", command=self.check_word)
        self.submit_button.pack()


        # Create a qwerty keyboard
        keyboard_frame = tk.Frame(master)
        keyboard_frame.pack()

        qwerty_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]

        
        for row in qwerty_layout:
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack()
            for letter in row:
                button = tk.Button(row_frame, text=letter, font=("Arial", 14), width=6, height=3,
                                   command=lambda l=letter: self.add_letter(l))
                button.pack(side=tk.LEFT, padx=5, pady=5)

        backspace_button = tk.Button(keyboard_frame, text="⌫", font=("Arial", 14), width=6, height=3,
                                     command=self.delete_letter)
        backspace_button.pack(side=tk.LEFT, padx=5, pady=5)
        


    def add_letter(self, letter):
        current_entry_text = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(tk.END, current_entry_text + letter)
        # Check if the letter is present in the target word
        if letter in self.target_word:
        # Set the button color to green
            for row in self.keyboard_buttons:
                for button in row:
                    if button["text"] == letter:
                        button.config(bg="green")
        else:
            # Set the button color to black
            for row in self.keyboard_buttons:
                for button in row:
                    if button["text"] == letter:
                        button.config(bg="black")

    def delete_letter(self):
        current_entry_text = self.input_entry.get()
        self.input_entry.delete(len(current_entry_text) - 1, tk.END)


    def check_word(self):
        guess = self.input_entry.get().upper()

        # Check if the guess is the same length as the target word
        if len(guess) != len(self.target_word):
            return

        self.attempts += 1

        # Update the grid with feedback
        for j in range(len(self.target_word)):
            letter = guess[j]
            if letter == self.target_word[j]:
                self.grid[self.attempts - 1][j].config(text=letter, bg="green")
            elif letter in self.target_word:
                self.grid[self.attempts - 1][j].config(text=letter, bg="yellow")
            else:
                self.grid[self.attempts - 1][j].config(text=letter, bg="grey")

        # Check if the word is correct
        if guess == self.target_word:
            self.target_label.config(text=self.target_word)
            self.input_entry.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.DISABLED)
            self.show_message("Congratulations! You guessed the word in {} attempts.".format(self.attempts), "You Won!")
        else:
            # Check if the player lost
            if self.attempts == self.max_attempts:
                self.input_entry.config(state=tk.DISABLED)
                self.submit_button.config(state=tk.DISABLED)
                self.show_message("Sorry! You lost the game. The correct word was {}.".format(self.target_word),
                                  "You Lost!")
    
    def show_message(self, message, title):
        result_window = tk.Toplevel(self.master)
        result_window.title(title)
        tk.Label(result_window, text=message, font=("Helvetica", 16)).pack(padx=20, pady=20)
        exit_button = tk.Button(result_window, text="Exit", command=self.master.destroy)
        exit_button.pack(pady=10)
        


def start_game():
    # Destroy the main window
    root.destroy()

    # Create the game window
    game_window = tk.Tk()
    game_window.title("Wordle Game")

    # Load the list of five-letter words from a file
    with open("five_letter_words.txt", "r") as f:
        words = [line.strip().upper() for line in f.readlines()]

    # Choose a random word from the list
    target_word = random.choice(words)

    # Initialize the WordleGame instance
    game = WordleGame(game_window, target_word)

    # Initialize pygame
    pygame.init()
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)

    # Start the game window's main event loop
    game_window.mainloop()

    # Stop the music when the game is over
    pygame.mixer.music.stop()


if _name_ == "_main_":
    root = tk.Tk()
    root.title("Wordle Game")
    root.attributes("-fullscreen", True)

    image_path = r"C:\Users\91939\Pictures\we.png"
    background_image = tk.PhotoImage(file=image_path)
    background_image = background_image.subsample(2)  # Adjust the factor as needed

    # Create a Label to display the background image
    background_label = tk.Label(image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a label for the game title
    title_label = tk.Label(root, text="Wordle Game", font=("Helvetica", 75, "bold"))
    title_label.pack(pady=120)

    # Create a button to start the game
    start_button = tk.Button(root, text="Start Game", command=start_game)
    start_button.pack()

    root.mainloop()