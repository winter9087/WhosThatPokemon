'''
Done by Leonie Riedel and Michelle Wallmann
Game: Who's that Pokémon?
Required files/folders: pokemon_data_new.py; pokemon_images_silhouette; pokemon_images_full 
Required external libraries: tkinter; pillow


incase anyone is wondering about the god awfull amount of comments in this code: my teacher requires it so

nidorans are nidoran without the ♀ signs
0669 Flabébé is flabebe
'''
import tkinter as tk
import os
import random
from PIL import Image, ImageTk # PIL (pillow) used to display .webp
from pokemon_data_new import pokemon_data # make sure data file is in same folder. is in seperate file so this is more readable

#whole game is in a class because OOP
class whosThatPokemon:
# initialise game function
    def __init__(self, root):
            self.root = root
            self.root.title("Who's the Pokémon?") #displayed in window title
            self.root.geometry("700x500") #might experiement with different sizes if time = True
            
            # all the important variables
            self.current_pokemon_name = "" # this is the english name that will be checked
            self.current_pokemon_name_german = "" # same thing but german (note from leonie: ew) 
            self.current_score = 0 # tracks consecutive right guesses 
            self.high_score = 0 # highest streak max should be smth like 1025/26
            self.time_left = 10 #timer 1 unit is 1 second
            self.remaining_pokemon = pokemon_data.copy() # use a temp list to make sure we only display each pokemon once
            self.timer_id = None  # timer ID to cancel the previous one to prevent a bug where timers would get faster
            self.mode = "normal"  # default mode is colour images

            # folder for colour images
            self.image_folder = "pokemon_images_full"

            # startup the selection screen
            self.setup_start_screen()
    
    def setup_start_screen(self):
        """starts up the start screen (haha) which allows to select mode and explains the game"""
        # start screen title
        self.title_label = tk.Label(self.root, text="Who's that Pokémon?", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # instructions because humans are le stupid
        self.instructions_label = tk.Label(
            self.root,
            text="Wähle einen Modus und klicke dann auf Start.\n"
                 "Schreibe den Namen des Pokémon's in Deutsch oder Englisch.\n"
                 "Du hast 10 Sekunden pro Pokémon.\n",
            font=("Arial", 14),
            justify="center"
        )
        self.instructions_label.pack(pady=20)

        # mode selection (normal or silhouette). radio buttons cause only one can be valid
        self.mode_label = tk.Label(self.root, text="Modus:")
        self.mode_label.pack(pady=10)

        self.mode_var = tk.StringVar(value="normal")
        self.normal_button = tk.Radiobutton(self.root, text="Normal", variable=self.mode_var, value="normal")
        self.normal_button.pack()
        self.silhouette_button = tk.Radiobutton(self.root, text="Silhouetten", variable=self.mode_var, value="silhouette")
        self.silhouette_button.pack()

        # start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 14))
        self.start_button.pack(pady=20)

    def start_game(self):
        """ starts the game."""
        # get the selected mode
        self.mode = self.mode_var.get()

        # obliterate start screen shit
        self.title_label.pack_forget()
        self.instructions_label.pack_forget()
        self.mode_label.pack_forget()
        self.normal_button.pack_forget()
        self.silhouette_button.pack_forget()
        self.start_button.pack_forget()

        #start game UI
        self.setup_game_ui()

        # load the first Pokémon
        self.load_new_pokemon()

    def setup_game_ui(self):
        """starts game UI components."""
        # image label
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        # input prompt
        self.input_label = tk.Label(self.root, text="Wie heißt dieses Pokémon (Deutsch oder Englisch):")
        self.input_label.pack()

        # Input field
        self.input_entry = tk.Entry(self.root)
        self.input_entry.pack(pady=5)

        # deedback label basically tells you if youre wrong or right
        self.feedback_label = tk.Label(self.root, text="")
        self.feedback_label.pack(pady=5)

        # score and time display
        self.status_label = tk.Label(self.root, text="Score: 0  |  Highscore: 0  |  Zeit übrig: 10", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # check button
        self.check_button = tk.Button(self.root, text="Check", command=self.check_input)
        self.check_button.pack(pady=10)

    def load_random_image(self):
        """load a random Pokémon  from the remaining list based on the selected mode"""
        if not self.remaining_pokemon: 
            self.end_game()
            return # none left? end the game duh

        # pick a random Pokémon
        random_pokemon = random.choice(self.remaining_pokemon)
        self.remaining_pokemon.remove(random_pokemon)
        self.current_pokemon_name = random_pokemon["name"]
        self.current_pokemon_name_german = random_pokemon["name_german"]

        # select the folder based on mode 
        folder = "pokemon_images_full" if self.mode == "normal" else "pokemon_images_silhouette"
        pokemon_image_key = 'image' if self.mode == "normal" else 'silhouette'
        pokemon_image = random_pokemon[pokemon_image_key]

        # construct the full path to the image
        image_path = os.path.join(folder, pokemon_image)

        # ensure the file exists before opening otherwise throw error
        if not os.path.isfile(image_path):
            self.feedback_label.config(text=f"Error: {pokemon_image} not found.", fg="red")
            return

        # load and display the image
        image = Image.open(image_path)
        image = image.resize((200, 200))  # resize so its all one size
        photo = ImageTk.PhotoImage(image)

        # update the image label
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # reset the timer
        self.time_left = 10
        self.update_timer()

    def check_input(self):
        """checks the user's input against the Pokémon's names."""
        user_input = self.input_entry.get().strip().lower()
        # the .lower is important so no matter the case of the input (eg. Bulbasaur or bulbasaur) the user is right
        if user_input == self.current_pokemon_name.lower() or user_input == self.current_pokemon_name_german.lower(): 
            self.current_score += 1 
            self.feedback_label.config(text="Korrekt!", fg="green") #if correct add to score and tell them theyre correct
        else:
            self.feedback_label.config(
                text=f"Falsch! Es war {self.current_pokemon_name.title()} / {self.current_pokemon_name_german.title()}.",
                fg="red"
            )
            # reset the score
            self.current_score = 0 #if theyre wrong tell them theye wrong and reset score

        # update the high score
        self.high_score = max(self.high_score, self.current_score)

        # update the score display
        self.update_status()

        # clear the input field
        self.input_entry.delete(0, tk.END)

        # load a new Pokémon
        self.load_new_pokemon()

    def update_timer(self):
        """Updates the timer and moves to the next Pokémon if time runs out."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_status()
            self.timer_id = self.root.after(1000, self.update_timer)  # store the timer ID
        else:
            # times up, reset score and load the next pokemon
            self.feedback_label.config(
                text=f"Zeit vorbei! Es war {self.current_pokemon_name.title()} / {self.current_pokemon_name_german.title()}.",
                fg="red"
            )
            self.current_score = 0
            self.update_status()
            self.load_new_pokemon()

    def update_status(self):
        """Updates the score and timer display."""
        self.status_label.config(
            text=f"Score: {self.current_score}  |  Highscore: {self.high_score}  |  Zeit übrig: {self.time_left}"
        )

    def load_new_pokemon(self):
        """loads a new Pokémon."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)  # Cancel the previous timer
        self.load_random_image()

    def end_game(self):
        """Ends the game when all Pokémon are used."""
        self.image_label.config(image="")
        self.feedback_label.config(text="Vorbei! Alle Pokémon wurden angezeigt.", fg="blue")
        self.status_label.config(
            text=f"Final Score: {self.current_score}  |  High Score: {self.high_score}"
        )
        self.check_button.config(state="disabled")

# Create the main application
if __name__ == "__main__":
    root = tk.Tk()
    app = whosThatPokemon(root)
    root.mainloop()
