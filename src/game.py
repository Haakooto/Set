from card import Card


class Game:
    """
    Game-instance hosted by server
    Controlls the current Cards on the board

    """
    def __init__(self, id):
        self.id = id  # game_id given by server
        self.deck = Card.generate_deck()
        self.active = []  # current Cards which should be on the board
        self.started = False  # False while waiting for players
        self.used_cards = 0  # how many Cards pulled from deck

    def __str__(self):
        return str(self.id)

    def start(self):
        """ Start game and fill the board """
        self.started = True
        for i in range(12):
            self.add_card(i)

    def add_card(self, i, extra=False):
        """ adds new card to actives """
        if len(self.active) <= 12 or not extra:
            self.active[i] = self.deck[self.used_cards].id  # simple replace
            self.used_cards += 1
        else:
            self.active.pop(i)  # remove without replace if too many
            # This solution will shift all cards on board after removed ones
            # May cause slight confusion for some players. No problem of mine ¯\_(ツ)_/¯
            # (yet)

    def add_extra(self):
        # Extend active if no set on board
        for i in range(3):
            self.add_card(i + len(self.active), True)

    def validate_set(self, idxs, player=False):
        # check if cards at indices in idxs form set
        # Is called to check if set even on board, or if player clicks 3 cards.
        # If called from player, also replace card if the form set
        a, b, c = [self.active[i] for i in idxs]
        valid = a.is_set(b, c)
        if valid and player:
            for n in idxs:
                self.add_card(n)
        return valid

    def set_on_board(self, check=False, help=False):
        # go throught every combination of cards on board to find if at least one set is on the board
        # Called by player when click on deck (blue numerated axes in corner), or if player asks for help
        cnt = len(self.cards_on_board)
        for i in range(cnt):
            for j in range(i + 1, cnt):
                for k in range(j + 1, cnt):
                    if self.validate_set(i, j, k):
                        if help:
                            return i, j, k
                        else:
                            return True
        if check:  # if called by player clicking deck and no sets on board:
            self.add_extra()  # add 3 extra
        # ! If not set on board while 3 extra are already there WILL cause problems. Handle this!
        return False
