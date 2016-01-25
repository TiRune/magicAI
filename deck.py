from Cards.card import Card
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import os


class Deck:
    def __init__(self, decklist):
        self.cards = []
        if type(decklist) == str:
            self.load_from_string(decklist)
        else:
            raise ValueError('given decklist is not a string, received instead:'
                             ' {}'.format(decklist))

    def load_from_string(self, decklist_name):
        self.cards = []

        decklist_location = 'Decklists/' + decklist_name
        stream = file(decklist_location,'r')
        decklist_dict = load(stream, Loader)

        for card_name, number in decklist_dict.iteritems():
            for _ in range(number):
                self.cards.append(Card(card_name))
