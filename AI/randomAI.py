from game_engine import GameEngine


class RandomAI():
    def __init__(self):
        self.engine = GameEngine()

    #def determine_eot_discard(self, hand):
    #    num_to_discard = len(hand.cards) - 7
    #    if num_to_discard <= 0:
    #        return []
    #    else:
    #        return rng.sample(range(len(hand.cards)), num_to_discard)

    def get_action(self, gamestate, player):
        if self.engine.current_phase_string(gamestate) == 'Pre-combat main phase':
            # play a land if possible
            for card in player.hand:
                if card.type == 'Land' and not gamestate.player_played_land:
                    return {'Play': card, "player": player.ID}
            # tap all lands for mana
            for card in player.battlefield:
                if card.untapped and card.type == 'Land':
                    return {'Use': card, "player": player.ID}

            # cast any cards we can
            for card in player.hand:
                if card.type == "Creature":
                    red_cost = card.cmc
                    if red_cost > 0:
                        if player.mana_pool >= red_cost:
                            return {'Play': card, "player": player.ID}
        return

    #def determine_attackers(self, gamestate, player):
    #    attackers = []
    #    for card in player.battlefield.cards:
    #        if card.type == "Creature":
    #            #if card.summoning_sickness is False:
    #            attackers.append(card)
    #    return attackers