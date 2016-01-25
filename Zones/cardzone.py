

class CardZone(object):
    def __init__(self):
        self.cards = []

    def __repr__(self):
        string = self.__name__ + ': ' + str(len(self.cards)) + ' ['
        for card in self.cards:
            string += card.__repr__() + ', '
        string = string[:-2] + ']'
        return string

    def set_cards(self, card_list):
        self.cards = card_list

    def add_card(self, card):
        self.cards.append(card)

    @property
    def num_cards(self):
        return len(self.cards)