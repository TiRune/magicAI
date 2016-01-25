import random as rng


class RandomAI():
    def __init__(self):
        pass

    def determine_eot_discard(self, hand):
        num_to_discard = len(hand.cards) - 7
        if num_to_discard <= 0:
            return []
        else:
            return rng.sample(range(len(hand.cards)), num_to_discard)

    def take_action(self, gamestate, player):
        if gamestate.current_phase_string == 'Pre-combat main phase' and \
                        gamestate.current_player.ID == player.ID:
                # play a land if possible
                for card in player.hand.cards:
                    if card.type == 'Land' and not gamestate.player_played_land:
                        return {'Play': card}
                # tap all lands for mana
                for card in player.battlefield.cards:
                    if card.untapped and card.type == 'Land':
                        return {'Use': card}

                # cast any cards we can
                for card in player.hand.cards:
                    red_cost = card.cmc.count('R')
                    if red_cost > 0:
                        if player.mana_pool.mana['red'] >= red_cost:
                            return {'Play': card}
        return None

    def determine_attackers(self, gamestate, player):
        attackers = []
        for card in player.battlefield.cards:
            if card.type == "Creature":
                if card.summoning_sickness is False:
                    attackers.append(card)
        return attackers