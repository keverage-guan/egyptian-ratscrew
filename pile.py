from card import Card

class Pile:
    """
    Represents a pile of cards in the game.
    """

    def __init__(self, rules=None):
        """
        Initialize a Pile object.

        Args:
            rules (dict, optional): A dictionary of game rules. Defaults to None.
        """
        self.cards = []
        self.bottom = None
        self.top = None
        self.under = None
        self.two_under = None
        self.rules = rules or {
            'Red 10': True,
            'Double Cards': True,
            'Double Value': True,
            'Add to 10': True,
            'Top-Bottom': True,
            'Marriage': True,
            'Divorce': True,
            'Staircase': True,
            'Sandwich': True
        }

    def add_card(self, card=None):
        """
        Add a card to the pile.

        Args:
            card (Card, optional): The card to add. If None, a random card is generated.
        """
        if card is None:
            card = Card.generate_card()
        self.cards.append(card)
        self.top = card
        self.bottom = self.cards[0]
        if len(self.cards) > 1:
            self.under = self.cards[-2]
        if len(self.cards) > 2:
            self.two_under = self.cards[-3]

    def clear(self):
        """Clear all cards from the pile."""
        self.cards = []

    def __len__(self):
        """Return the number of cards in the pile."""
        return len(self.cards)
    
    def slap(self):
        """
        Check if the current state of the pile allows for a slap.

        Returns:
            str: The type of slap if valid, 'No Slap' otherwise.
        """
        # one card
        if self.rules['Red 10'] and (self.top.card == '10' and self.top.color == 'red'):
            return 'Red 10'
        if self.under is None:
            return 'No Slap'
        
        # two cards
        if self.rules['Double Cards'] and self.top.card == self.under.card:
            return 'Double Cards'
        if self.top.card.isnumeric() and self.under.card.isnumeric():
            top_val, under_val = int(self.top.card), int(self.under.card)
            if self.rules['Double Value'] and (top_val == 2 * under_val or under_val == 2 * top_val):
                return 'Double Value'
            if self.rules['Add to 10'] and (top_val + under_val == 10):
                return 'Add to 10'    
        if self.rules['Top-Bottom'] and self.top.card == self.bottom.card:
            return 'Top-Bottom'
        if self.rules['Marriage'] and set([self.top.card, self.under.card]) == set(['K', 'Q']):
            return 'Marriage'
        if self.two_under is None:
            return 'No Slap'

        # three cards
        if self.rules['Divorce'] and set([self.top.card, self.two_under.card]) == set(['K', 'Q']):
            return 'Divorce'
        if self.rules['Staircase'] and staircase([self.top, self.under, self.two_under]):
            return 'Staircase'
        if self.rules['Sandwich'] and self.top.card == self.two_under.card:
            return 'Sandwich'
        return 'No Slap'

def staircase(cards):
    """
    Check if three cards form a staircase (ascending or descending sequence).

    Args:
        cards (list): List of three Card objects.

    Returns:
        bool: True if cards form a staircase, False otherwise.
    """
    if cards[0].value + 1 == cards[1].value and cards[1].value + 1 == cards[2].value:
        return True
    if cards[0].value - 1 == cards[1].value and cards[1].value - 1 == cards[2].value:
        return True
    return False