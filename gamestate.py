from player import Player

class GameState:
    def __init__(self):
        self.phase = 0
        self.player_turn = 0
        self.player_played_land = False
        self.turn = 1
        self.players = [Player(0), Player(1)]