from .card import Card
from itertools import combinations


class Game:
    """
    Game-instance hosted by server
    Controlls the current Cards on the board

    """

    def __init__(self, id):
        """ Init game with deck of cards """
        self.id = id  # game_id given by server
        self.inactive = 0
        self.deck = Card.generate_deck()
        self.active = [None for i in range(15)]  # idxs if card in deck which should be on the board
        self.started = False  # False while waiting for players
        self.used_cards = 0  # how many Cards pulled from deck
        self.other_msg = None
        self.extra = False
        self.game_over = False

    def __str__(self):
        return str(self.id)

    def get_active_ids(self):
        return [self.deck[i].id if i is not None else None for i in self.active]

    def remaining(self):
        if self.used_cards is None:
            return 0
        else:
            return 81 - self.used_cards

    def start(self):
        """ Start game and fill the board """
        self.started = True
        for i in range(12):
            self.add_card(i)
        return self.started

    def add_card(self, i, extra=False):
        """
        removes and adds cards to board.

        Cards on board exist in list, index in list correspond to place on board
        Normally replaces the card at relavent index
        Can also extend board to 15 cards if needed
        """
        if sum([j is not None for j in self.active]) <= 12 or extra:
            self.active[i] = self.used_cards
            if self.used_cards == 80:
                self.used_cards = None
            elif self.used_cards is not None:
                self.used_cards += 1
        else:
            self.active[i] = None

    def add_extra(self):
        """When no set on board, add 3 more cards """
        self.extra = True
        for i in range(3):
            self.add_card(12 + i, True)

    def move(self):
        for i, card in enumerate(self.active[12:]):
            if card is not None:
                self.active[self.active.index(None)] = card
                self.active[i + 12] = None
                self.extra = False

    def validate_set(self, idxs, player=False):
        # check if cards at given indices form set
        # Is called to check if set even on board, or if player clicks 3 cards.
        # If called by player, then replace cards if they form set
        a, b, c = [self.deck[self.active[i]] for i in idxs]
        valid = a.form_set(b, c)
        if valid and player:
            for n in idxs:
                self.add_card(n)
            self.move()
            self.end_game()
        return valid

    def end_game(self):
        if self.used_cards is None:
            if not self.set_on_board():
                self.game_over = True
        elif self.extra and not self.set_on_board():
            self.game_over = True

    def set_on_board(self, check=False, help=False):
        # loop through every combinatin of cards on board to determine if there's at leat 1 set
        # check=True if deck is clicked, climing there are no sets on board, in which case extra are added
        # help is debug-function, player asking for help
        for i, j, k in combinations(range(15), 3):
            if None in [self.active[n] for n in (i, j, k)]:
                continue
            elif self.validate_set((i, j, k)):
                if help:
                    return i, j, k
                else:
                    return True
        if check:  # player click in deck
            if self.extra: # if true, would end game. Handled by end_game()
                self.other_msg = ""
            else:
                self.add_extra()
        return False
