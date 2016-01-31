class Player:
    def __init__(self, ID):
        self.library = []
        self.battlefield = []
        self.hand = []
        self.graveyard = []
        self.lost = False
        self.life = 20
        self.empty_draw_attempt = None
        self.mana_pool = 0
        self.ID = ID