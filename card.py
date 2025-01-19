import random

class Card:
    """
    Represents a playing card with a suite and value.
    """

    def __init__(self, suite, card):
        """
        Initialize a Card object.

        Args:
            suite (str): The suite of the card (Hearts, Diamonds, Clubs, Spades).
            card (str): The value of the card (2-10, J, Q, K, A).
        """
        card_vals = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        self.suite = suite
        self.card = card
        self.value = card_vals[card]
        self.color = 'red' if suite in ['Hearts', 'Diamonds'] else 'black'

    def __repr__(self):
        """Return a string representation of the card."""
        return f'{self.suite}{self.card}'
    
    def __lt__(self, other):
        """Compare cards based on their value."""
        return self.value < other.value

    def filename(self):
        """Return the filename for the card's image."""
        return f'card{self.suite}{self.card}.png'

    @staticmethod
    def generate_card():
        """Generate a random card."""
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suites = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        return Card(random.choice(suites), random.choice(cards))