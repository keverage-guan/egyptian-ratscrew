import tkinter as tk
from PIL import Image, ImageTk
from pile import Pile
import time

class CardGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Card Game")
        self.master.geometry("300x450")

        self.pile = Pile()
        
        self.card_label = tk.Label(master)
        self.card_label.pack(pady=20)

        self.info_label = tk.Label(master, text="", font=("Arial", 14))
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