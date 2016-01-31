
from errors import GameStateError, GameRuleViolation
import random

class GameEngine:
    def __init__(self):
        self.phases = ['Untap Step', 'Upkeep Step', 'Draw Step', 'Pre-combat main phase', 'Beginning of combat', 'Declare attackers step', 'Declare blockers step', 'Combat damage step', 'End of combat step', 'Post-combat main phase', 'End step', 'Cleanup step']
        self.phases_dict = dict(enumerate(self.phases))

    def current_phase_string(self, gamestate):
        return self.phases_dict[gamestate.phase]

    def setup_game(self, gamestate, deck_1, deck_2):
        random.shuffle(deck_1)
        random.shuffle(deck_2)
        gamestate.players[0].library = deck_1
        gamestate.players[1].library = deck_2

        for player in gamestate.players:
            for _ in range(7):
                player.hand.append(player.library.pop())
            player.life = 20

    def game_over(self, gamestate):
        number_lost = 0
        for player in gamestate.players:
            if player.lost:
                number_lost += 1
        if number_lost >= len(gamestate.players) - 1:
            return True
        else:
            return False

    def action_play(self, card, player_num, gamestate):
        performing_player = gamestate.players[player_num]
        for i in range(len(performing_player.hand)):
            if performing_player.hand[i] == card:
                if card.type == 'Land':
                    if gamestate.player_played_land:
                        raise GameRuleViolation('Can\'t play two '
                                                'lands in a turn')
                    gamestate.player_played_land = True

                print performing_player.mana_pool
                print card.cmc
                performing_player.mana_pool -= card.cmc

                move_card = performing_player.hand.pop(i)
                move_card.summoning_sickness = True
                move_card.tapped = False
                performing_player.battlefield.append(move_card)
                break

    def action_use(self, cards_to_use, player_num, gamestate):
        performing_player = gamestate.players[player_num]
        for i in range(len(performing_player.battlefield)):
            for card in cards_to_use:
                if performing_player.battlefield[i] == card:
                    if card.tapped:
                        raise GameRuleViolation('trying to use a card that '
                                                'is already tapped')
                    if card.type == 'Land' and card.subtypes == 'Mountain':
                        card.tapped = True
                        performing_player.mana_pool += 1

    def empty_all_manapools(self, gamestate):
        for player in gamestate.players:
            player.mana_pool = 0

    def non_active_player(self, gamestate):
        return gamestate.players[abs(gamestate.player_turn - 1)]

    def deal_combat_damage(self, gamestate):
        for creature in self.current_player(gamestate).battlefield:
            if creature.attacking:
                defending_player = self.non_active_player(gamestate)
                defending_player.life -= creature.power

    def current_player(self, gamestate):
        return gamestate.players[gamestate.player_turn]

    def handle_untap_step(self, gamestate):
        self.empty_all_manapools(gamestate)
        player = self.current_player(gamestate)
        for card in player.battlefield:
            card.tapped = False
            card.summoning_sickness = False
        return False

    def handle_upkeep_step(self, gamestate):
        return False

    def draw(self, player):
        if len(player.library) > 0:
            card = player.library.pop(0)
            player.hand.append(card)
        else:
            player.empty_draw_attempt = True

    def handle_draw_step(self, gamestate):
        self.draw(self.current_player(gamestate))
        return False

    def handle_precombat_main_phase(self, gamestate):
        self.empty_all_manapools(gamestate)
        return True

    def handle_beginning_of_combat(self, gamestate):
        self.empty_all_manapools(gamestate)
        return False

    def handle_declare_attackers(self, gamestate):
        return True

    def handle_declare_blockers(self, gamestate):
        return False

    def handle_combat_damage(self, gamestate):
        self.deal_combat_damage(gamestate)

    def handle_end_of_combat(self, gamestate):
        return False

    def handle_postcombat_main_phase(self, gamestate):
        # remove all creatures from combat
        player = self.current_player(gamestate)
        for card in player.battlefield:
            card.attacking = False
        return False

    def handle_end_step(self, gamestate):
        self.empty_all_manapools(gamestate)
        return False

    def handle_cleanup_step(self, gamestate):
        gamestate.player_played_land = False
        return False

    def put_in_graveyard_from_play(self, card, player):
        for i in range(len(player.battlefield.cards)):
            if card == player.battlefield.cards[i]:
                player.battlefield.cards.pop(i)
                player.graveyard.add_card(card)


    def check_state_based_actions(self, gamestate):
        # 704.5a If a player has 0 or less life, he or she loses the game.
        for player in gamestate.players:
            if not player.life > 0:
                player.lost = True

        # 704.5b If a player attempted to draw a card from a library with no
        # cards in it since the last time state-based actions were checked,
        # he or she loses the game.
        for player in gamestate.players:
            if player.empty_draw_attempt:
                player.lost = True

        # 704.5f If a creature has toughness 0 or less, it's put into
        # its owner's graveyard. Regeneration can't replace this event.
        # 704.5g If a creature has toughness greater than 0, and the total
        # damage marked on it is greater than or equal to its toughness,
        # that creature has been dealt lethal damage and is destroyed.
        # Regeneration can replace this event.
        for player in gamestate.players:
            for card in player.battlefield:
                if card.type == "Creature":
                    if card.toughness <= 0:
                        self.put_in_graveyard_from_play(card, player)
                    elif card.damage >= card.toughness:
                        self.put_in_graveyard_from_play(card, player)

    def next_phase(self, gamestate):
        gamestate.phase += 1
        if gamestate.phase / len(self.phases) != 0:
            gamestate.phase -= len(self.phases)
            gamestate.player_turn = (gamestate.player_turn + 1) % \
                                    len(gamestate.players)
            gamestate.turn += 1

    def handle_phase_until_action(self, gamestate):

        action_moment = False
        while not action_moment:
            phase_number = gamestate.phase
            if phase_number == 0:
                action_moment = self.handle_untap_step(gamestate)
            elif phase_number == 1:
                action_moment = self.handle_upkeep_step(gamestate)
            elif phase_number == 2:
                action_moment = self.handle_draw_step(gamestate)
            elif phase_number == 3:
                action_moment = self.handle_precombat_main_phase(gamestate)
            elif phase_number == 4:
                action_moment = self.handle_beginning_of_combat(gamestate)
            elif phase_number == 5:
                action_moment = self.handle_declare_attackers(gamestate)
            elif phase_number == 6:
                action_moment = self.handle_declare_blockers(gamestate)
            elif phase_number == 7:
                action_moment = self.handle_combat_damage(gamestate)
            elif phase_number == 8:
                action_moment = self.handle_end_of_combat(gamestate)
            elif phase_number == 9:
                action_moment = self.handle_postcombat_main_phase(gamestate)
            elif phase_number == 10:
                action_moment = self.handle_end_step(gamestate)
            elif phase_number == 11:
                action_moment = self.handle_cleanup_step(gamestate)
            else:
                raise ValueError("phase_number unknown")

            self.check_state_based_actions(gamestate)
            if self.game_over(gamestate):
                return

            if not action_moment:
                self.next_phase(gamestate)

    def who_has_action(self, gamestate):
        return gamestate.player_turn

    def can_attack(self, creature, gamestate):
        if not creature.summoning_sickness:
            return True
        else:
            return False

    def action_attack(self, attackers, player, gamestate):
        for creature in attackers:
            if self.can_attack(creature, gamestate):
                creature.attacking = True
            else:
                return GameRuleViolation(
                        "Can't attack with {}".format(creature))

    def take_action(self, gamestate, action):
        print action
        if not action or action == "pass_priority":
            self.next_phase(gamestate)
            self.handle_phase_until_action(gamestate)
            return
        elif 'Play' in action:
                self.action_play(action['Play'], action['player'], gamestate)
        elif 'Use' in action:
                self.action_use(action['Use'], action['player'], gamestate)
        elif 'Attack' in action:
                self.action_attack(action['Attack'], action['player'], gamestate)
                self.next_phase(gamestate)
                self.handle_phase_until_action(gamestate)