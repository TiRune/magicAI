from deck import Deck
from Zones import Library, Hand, Graveyard, Battlefield
from manapool import ManaPool

class Player:
    def __init__(self, ID):
        self.library = Library()
        self.battlefield = Battlefield()
        self.hand = Hand()
        self.graveyard = Graveyard()
        self.exile = []
        self.deck = None
        self.lost = False
        self.AI = None
        self.life = 20
        self.empty_draw_attempt = False
        self.mana_pool = ManaPool()
        self.ID = ID

    def set_deck(self, deck_name):
        self.deck = Deck(deck_name)

    def setup_library(self):
        if not self.deck:
            raise ValueError("Deck not setup properly before game start")
        self.library.set_cards(self.deck.cards)

    def set_life_total(self, life):
        self.life = life

    def shuffle_deck(self):
        self.library.shuffle()

    def draw_cards(self, num_cards):
        for _ in range(num_cards):
            self.draw()

    @property
    def positive_life(self):
        if self.life > 0:
            return True

    def draw(self):
        if self.library.num_cards <= 0:
            self.empty_draw_attempt = True
        self.library.draw(self.hand)

    def set_AI(self, AI):
        self.AI = AI

    def discard(self, number):
        card = self.hand.cards.pop(number)
        self.graveyard.cards.append(card)

    def discard_list(self, num_cards_to_discard):
        for i in num_cards_to_discard:
            self.discard(i)

    def eot_discard(self):
        num_cards_to_discard = self.AI.determine_eot_discard(self.hand)
        self.discard_list(num_cards_to_discard)

    def empty_manapool(self):
        self.mana_pool.empty_pool()


    def take_action(self, game_state):
        action = self.AI.take_action(game_state, self)
        if action:
            action['player'] = self.ID
        else:
            action = {'pass_priority': 1}
        return action

    def determine_attackers(self, game_state):
        attackers = self.AI.determine_attackers(game_state, self)
        return attackers