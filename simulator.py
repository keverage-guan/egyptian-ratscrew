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
            'Sandwich': tk.BooleanVar(value=True),
            'Autoplay': tk.BooleanVar(value=True)
        }

        self.card_delay = tk.StringVar(value="1.0")
        self.slap_time = tk.StringVar(value="1.0")

        self.create_settings_screen()
        self.state = 'IDLE'
        self.slap_timer = None

    def create_settings_screen(self):
        self.settings_frame = ttk.Frame(self.master, padding="10")
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.settings_frame, text="Select Rules", font=("Arial", 16)).pack(pady=10)

        for rule, var in self.rules.items():
            ttk.Checkbutton(self.settings_frame, text=rule, variable=var).pack(anchor='w')

        ttk.Label(self.settings_frame, text="Time between cards (seconds):").pack(anchor='w', pady=(10, 0))
        ttk.Entry(self.settings_frame, textvariable=self.card_delay, width=5).pack(anchor='w')

        ttk.Label(self.settings_frame, text="Time to slap (seconds):").pack(anchor='w', pady=(10, 0))
        ttk.Entry(self.settings_frame, textvariable=self.slap_time, width=5).pack(anchor='w')

        ttk.Button(self.settings_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.settings_frame.destroy()
        self.pile.rules = {rule: var.get() for rule, var in self.rules.items()}
        self.autoplay = self.rules['Autoplay'].get()

        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.game_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.card_label = tk.Label(self.canvas, bg='white')
        self.card_label.pack(pady=20)

        self.info_label = tk.Label(self.canvas, text="", font=("Arial", 14), bg='white')
        self.info_label.pack(pady=20)

        if not self.autoplay:
            self.master.bind('<space>', self.handle_slap)

        self.card_delay_ms = int(float(self.card_delay.get()) * 1000)
        self.slap_time_ms = int(float(self.slap_time.get()) * 1000)

        self.next_card()

    def next_card(self):
        self.state = 'SHOWING_CARD'
        self.pile.add_card()
        card = self.pile.top
        
        image_path = f"cards/{card.filename()}"
        try:
            image = Image.open(image_path)
            image = image.resize((200, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.card_label.config(image=photo)
            self.card_label.image = photo
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
            self.card_label.config(text=f"{card}")

        self.info_label.config(text="")
        self.set_background_color('white')
        
        self.slap_result = self.pile.slap()
        
        if self.autoplay:
            if self.slap_result != 'No Slap':
                self.master.after(self.slap_time_ms, self.show_slap, self.slap_result)
            else:
                self.master.after(self.card_delay_ms, self.next_card)
        else:
            if self.slap_result != 'No Slap':
                self.slap_timer = self.master.after(self.slap_time_ms, self.check_missed_slap)
            else:
                self.slap_timer = self.master.after(self.card_delay_ms, self.next_card)
    def handle_slap(self, event):
        if self.state == 'WAITING_FOR_SLAP' or self.state == 'SHOWING_CARD':
            if self.slap_timer:
                self.master.after_cancel(self.slap_timer)
            if self.slap_result != 'No Slap':
                self.show_slap(self.slap_result)
            else:
                self.show_no_slap()

    def show_slap(self, slap_result):
        self.state = 'SHOWING_RESULT'
        self.set_background_color('green')
        self.info_label.config(text=f"Slap: {slap_result}")
        self.master.after(1000, self.restart_game)

    def show_no_slap(self):
        self.state = 'SHOWING_RESULT'
        self.set_background_color('red')
        self.info_label.config(text="No Slap")
        self.master.after(1000, self.schedule_next_card)

    def check_missed_slap(self):
        self.state = 'SHOWING_RESULT'
        self.set_background_color('red')
        self.info_label.config(text=f"Missed Slap: {self.slap_result}")
        self.master.after(1000, self.schedule_next_card)

    def schedule_next_card(self):
        self.master.after(self.card_delay_ms, self.next_card)

    def restart_game(self):
        self.pile = Pile()
        self.pile.rules = {rule: var.get() for rule, var in self.rules.items()}
        self.schedule_next_card()

    def set_background_color(self, color):
        if color == 'green':
            pastel_color = '#90EE90'  # Light green
        elif color == 'red':
            pastel_color = '#FFB3BA'  # Light red (pink)
        else:
            pastel_color = color  # Use the original color if it's not green or red

        self.canvas.config(bg=pastel_color)
        self.card_label.config(bg=pastel_color)
        self.info_label.config(bg=pastel_color)

def main():
    root = tk.Tk()
    game = CardGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()