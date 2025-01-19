
import random
import time
from pile import Pile
from card import Card

def simulate_random(n=100, delay=1):
    pile = Pile()
    for i in range(n):
        pile.add_card()
        print(pile.cards[-1].filename())
        time.sleep(delay)
        print(pile.slap())
        time.sleep(delay)

def simulate(cards):
    pile = Pile()
    for card in cards:
        pile.add_card(card)
        print(pile.cards[-1].filename())
        time.sleep(1)
        print(pile.slap())
        time.sleep(1)

suites = ['Hearts', 'Hearts', 'Hearts']
cards = ['7', '6', '5']

card_list = [Card(suite, card) for suite, card in zip(suites, cards)]

simulate(card_list)