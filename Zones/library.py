from cardzone import CardZone
from random import shuffle


class Library(CardZone):

    def __init__(self):
        super(self.__class__, self).__init__()

    def shuffle(self):
        shuffle(self.cards)

    def draw(self, hand):
        if len(self.cards) > 0:
            card_to_draw = self.cards.pop(0)
            hand.add_card(card_to_draw)

    @property
    def __name__(self):
        return 'Library'