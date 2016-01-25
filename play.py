from gamestate import GameState
from AI.randomAI import RandomAI


gamestate = GameState()

gamestate.player_1.set_deck('goblins.deck')
gamestate.player_2.set_deck('goblins.deck')

gamestate.player_1.set_AI(RandomAI())
gamestate.player_2.set_AI(RandomAI())

gamestate.play()
