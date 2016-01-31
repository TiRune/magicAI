from game_engine import GameEngine


class RandomAI():
    def __init__(self):
        self.engine = GameEngine()

    def get_action(self, gamestate, player):
        if self.engine.current_phase_string(gamestate) == 'Pre-combat main phase':
            # play a land if possible
            for card in player.hand:
                if card.type == 'Land' and not gamestate.player_played_land:
                    return {'Play': card, "player": player.ID}
            # tap all lands for mana
            use_cards = []
            for card in player.battlefield:
                if card.untapped and card.type == 'Land':
                    use_cards.append(card)
            if use_cards:
                return {'Use': use_cards, "player": player.ID}

            # cast any cards we can
            for card in player.hand:
                if card.type == "Creature":
                    if player.mana_pool >= card.cmc:
                        return {'Play': card, "player": player.ID}
            return "pass_priority"
        elif self.engine.current_phase_string(gamestate) == 'Declare attackers step':
            attackers = []
            for card in player.battlefield:
                if card.type == "Creature":
                    if card.summoning_sickness is False:
                        attackers.append(card)
            return {'Attack': attackers, "player": player.ID}