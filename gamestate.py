from player import Player

from errors import GameStateError, GameRuleViolation


class GameState:
    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.started = False
        self.phase = None
        self.phases = ['Untap Step', 'Upkeep Step', 'Draw Step', 'Pre-combat main phase', 'Beginning of combat', 'Declare attackers step', 'Declare blockers step', 'Combat damage step', 'End of combat step', 'Post-combat main phase', 'End step', 'Cleanup step']
        self.phases_dict = dict(enumerate(self.phases))
        self.player_turn = 0
        self.player_played_land = False
        self.turn = 1

    @property
    def current_phase_string(self):
        return self.phases_dict[self.phase]

    @property
    def num_players(self):
        return len(self.players)

    @property
    def current_player(self):
        return self.players[self.player_turn]

    @property
    def other_players(self):
        return self.players[:self.player_turn] + \
               self.players[self.player_turn+1:]

    @property
    def player_1(self):
        return self.players[0]

    @property
    def player_2(self):
        return self.players[1]

    def take_pregame_actions(self):
        for player in self.players:
            player.setup_library()
            player.shuffle_deck()
            player.draw_cards(7)
            player.set_life_total(20)

    def game_over(self):
        number_lost = 0
        for player in self.players:
            if player.lost:
                number_lost += 1
        if number_lost >= len(self.players) - 1:
            return True
        else:
            return False

    def action_play(self, card, player_num):
        performing_player = self.players[player_num]
        for i in range(len(performing_player.hand.cards)):
            if performing_player.hand.cards[i] == card:
                if card.type == 'Land':
                    if self.player_played_land:
                        raise GameRuleViolation('Can\'t play two '
                                                'lands in a turn')
                    self.player_played_land = True

                performing_player.mana_pool.reduce_by(card.cmc)

                move_card = performing_player.hand.cards.pop(i)
                move_card.summoning_sickness = True
                performing_player.battlefield.cards.append(move_card)

                break

    def action_use(self, card, player_num):
        performing_player = self.players[player_num]
        for i in range(len(performing_player.battlefield.cards)):
            if performing_player.battlefield.cards[i] == card:
                if card.tapped:
                    raise GameRuleViolation('trying to use a card that '
                                            'is already tapped')
                if card.type == 'Land' and card.subtypes == 'Mountain':
                    card.tapped = True
                    performing_player.mana_pool.add('R')

    def process_action(self, action):
        if action:
            if 'Play' in action:
                self.action_play(action['Play'], action['player'])
            if 'Use' in action:
                self.action_use(action['Use'], action['player'])

    def action_until_priorities_passed(self):
        priorities_passed = 0
        while priorities_passed < self.num_players:
            for player in self.player_priority_order:
                action = player.take_action(self)
                self.process_action(action)
                if 'pass_priority' in action:
                    priorities_passed += 1
                else:
                    priorities_passed = 0

    def empty_all_manapools(self):
        for player in self.players:
            player.empty_manapool()

    def assign_attackers(self, attackers):
        for creature in attackers:
            if not creature.type == 'Creature':
                raise GameStateError("Attacking with a card that is not "
                                     "a creature")
            if creature in self.current_player.battlefield.cards:
                if creature.summoning_sickness:
                    raise GameRuleViolation("Tried to attack with a creature "
                                            "that has summoning sickness")
                creature.attacking = True
            else:
                raise GameStateError("Tried to attack with a creature not "
                                      "on player's side of the battlefield")

    def deal_combat_damage(self):
        for creature in self.current_player.battlefield.cards:
            if creature.attacking:
                defending_player = self.other_players[0]
                defending_player.life -= creature.power

    def handle_untap_step(self):
        self.empty_all_manapools()
        self.check_state_based_actions()
        for player in self.players:
            for card in player.battlefield.cards:
                card.tapped = False
                card.summoning_sickness = False

    def handle_upkeep_step(self):
        self.check_state_based_actions()

    def handle_draw_step(self):
        self.current_player.draw()
        self.check_state_based_actions()

    @property
    def player_priority_order(self):
        return self.players[self.player_turn:] + \
               self.players[:self.player_turn]

    def handle_precombat_main_phase(self):
        self.empty_all_manapools()
        self.check_state_based_actions()
        self.action_until_priorities_passed()

    def handle_beginning_of_combat(self):
        self.empty_all_manapools()
        self.check_state_based_actions()

    def handle_declare_attackers(self):
        attackers = self.current_player.determine_attackers(self)
        self.assign_attackers(attackers)
        self.check_state_based_actions()

    def handle_declare_blockers(self):
        self.check_state_based_actions()

    def handle_combat_damage(self):
        self.check_state_based_actions()
        self.deal_combat_damage()

    def handle_end_of_combat(self):
        self.check_state_based_actions()

    def handle_postcombat_main_phase(self):
        self.empty_all_manapools()
        self.check_state_based_actions()

    def handle_end_step(self):
        self.empty_all_manapools()
        self.check_state_based_actions()

    def handle_cleanup_step(self):
        if self.current_player.hand.num_cards > 7:
            self.current_player.eot_discard()
            if self.current_player.hand.num_cards > 7:
                raise GameStateError("Not enough cards discarded in cleanup")
        self.player_played_land = False

    def put_in_graveyard_from_play(self, card, player):
        for i in range(len(player.battlefield.cards)):
            if card == player.battlefield.cards[i]:
                player.battlefield.cards.pop(i)
                player.graveyard.add_card(card)


    def check_state_based_actions(self):
        # 704.5a If a player has 0 or less life, he or she loses the game.
        for player in self.players:
            if not player.positive_life:
                player.lost = True

        # 704.5b If a player attempted to draw a card from a library with no
        # cards in it since the last time state-based actions were checked,
        # he or she loses the game.
        for player in self.players:
            if player.empty_draw_attempt:
                player.lost = True

        # 704.5f If a creature has toughness 0 or less, it's put into
        # its owner's graveyard. Regeneration can't replace this event.
        # 704.5g If a creature has toughness greater than 0, and the total
        # damage marked on it is greater than or equal to its toughness,
        # that creature has been dealt lethal damage and is destroyed.
        # Regeneration can replace this event.
        for player in self.players:
            for card in player.battlefield.cards:
                if card.type == "Creature":
                    if card.toughness <= 0:
                        self.put_in_graveyard_from_play(card, player)
                    elif card.damage >= card.toughness:
                        self.put_in_graveyard_from_play(card, player)



    def handle_phase(self, phase_number):
        if phase_number == 0:
            self.handle_untap_step()
        elif phase_number == 1:
            self.handle_upkeep_step()
        elif phase_number == 2:
            self.handle_draw_step()
        elif phase_number == 3:
            self.handle_precombat_main_phase()
        elif phase_number == 4:
            self.handle_beginning_of_combat()
        elif phase_number == 5:
            self.handle_declare_attackers()
        elif phase_number == 6:
            self.handle_declare_blockers()
        elif phase_number == 7:
            self.handle_combat_damage()
        elif phase_number == 8:
            self.handle_end_of_combat()
        elif phase_number == 9:
            self.handle_postcombat_main_phase()
        elif phase_number == 10:
            self.handle_end_step()
        elif phase_number == 11:
            self.handle_cleanup_step()
        else:
            raise ValueError("phase_number unknown")

    def next_phase(self):
        self.phase += 1
        if self.phase / len(self.phases) != 0:
            self.phase -= len(self.phases)
            self.player_turn = (self.player_turn + 1) % len(self.players)
            self.turn += 1

        self.handle_phase(self.phase)

    def play(self):
        if not self.started:
            self.started = True
            self.take_pregame_actions()
            self.phase = 2
            self.player_turn = 0
            self.turn = 1

        while not self.game_over():
            self.next_phase()

            print self.current_phase_string, 'player\'s turn: ', \
                self.player_turn, 'turn: ', self.turn
            print 'Life: ', self.player_1.life
            print 'Library: ', len(self.player_1.library.cards)
            print self.player_1.hand
            print self.player_1.battlefield
            print self.player_1.mana_pool
            print 'Library: ', len(self.player_2.library.cards)
            print 'Life: ', self.player_2.life
            print self.player_2.hand
            print self.player_2.battlefield
            print self.player_2.mana_pool
            print '-------------------------'
