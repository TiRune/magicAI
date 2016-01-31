from game_engine import GameEngine
from gamestate import GameState
from AI.randomAI import RandomAI
from deck import Deck

game_engine = GameEngine()
AI_1 = RandomAI()
AI_2 = RandomAI()

deck_1 = Deck('goblins.deck').cards
deck_2 = Deck('goblins.deck').cards

gamestate = GameState()

game_engine.setup_game(gamestate, deck_1, deck_2)

while not game_engine.game_over(gamestate):
    if game_engine.who_has_action(gamestate) == 0:
        action = AI_1.get_action(gamestate, gamestate.players[0])
    else:
        action = AI_2.get_action(gamestate, gamestate.players[1])
    game_engine.take_action(gamestate, action)

    print "-------------------------------------------------------------------"
    print "turn: ", gamestate.turn, "phase:", game_engine.current_phase_string(gamestate)
    print "life: ", gamestate.players[1].life, "mana", gamestate.players[1].mana_pool, "library: ", len(gamestate.players[1].library)
    print "player_1_hand", gamestate.players[1].hand
    print "player_1_battlefield", gamestate.players[1].battlefield
    print "player_0_battlefield", gamestate.players[0].battlefield
    print "player_0_hand", gamestate.players[0].hand
    print "life: ", gamestate.players[0].life, "mana", gamestate.players[0].mana_pool, "library: ", len(gamestate.players[0].library)

print "player_0 lost: ", gamestate.players[0].lost