import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pile import Pile
import time

class CardGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Card Game")
        self.master.geometry("300x450")

        self.pile = Pile()
        self.rules = {
            'Red 10': tk.BooleanVar(value=True),
            'Double Cards': tk.BooleanVar(value=True),
            'Double Value': tk.BooleanVar(value=True),
            'Add to 10': tk.BooleanVar(value=True),
            'Top-Bottom': tk.BooleanVar(value=True),
            'Marriage': tk.BooleanVar(value=True),
            'Divorce': tk.BooleanVar(value=True),
            'Staircase': tk.BooleanVar(value=True),
            'Sandwich': tk.BooleanVar(value=True)
        }

        self.create_settings_screen()

    def create_settings_screen(self):
        self.settings_frame = ttk.Frame(self.master, padding="10")
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.settings_frame, text="Select Rules", font=("Arial", 16)).pack(pady=10)

        for rule, var in self.rules.items():
            ttk.Checkbutton(self.settings_frame, text=rule, variable=var).pack(anchor='w')

        ttk.Button(self.settings_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.settings_frame.destroy()
        self.pile.rules = {rule: var.get() for rule, var in self.rules.items()}

        self.card_label = tk.Label(self.master)
        self.card_label.pack(pady=20)

        self.info_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.info_label.pack(pady=20)

        self.next_card()

    def next_card(self):
        self.pile.add_card()
        card = self.pile.top
        
        # Load and display the card image
        image_path = f"cards/{card.filename()}"
        image = Image.open(image_path)
        image = image.resize((200, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.card_label.config(image=photo)
        self.card_label.image = photo

        self.info_label.config(text="")
        
        slap_result = self.pile.slap()
        if slap_result != 'No Slap':
            self.master.after(1000, self.show_slap, slap_result)
        else:
            self.master.after(1000, self.next_card)

    def show_slap(self, slap_result):
        self.info_label.config(text=f"Slap: {slap_result}")
        self.master.after(1000, self.next_card)

def main():
    root = tk.Tk()
    game = CardGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()