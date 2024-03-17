from card import Card


class Game:
    """
    Game-instance hosted by server
    Controlls the current Cards on the board

    """
    def __init__(self):
        self.inactive = 0
        self.deck = Card.generate_deck()
        self.active = [None for i in range(15)]  # idxs if card in deck which should be on the board
        self.started = False  # False while waiting for players
        self.used_cards = 0  # how many Cards pulled from deck
        self.other_msg = None
        self.extra = False
        self.points = 0

    def get_active_ids(self):
        return [self.deck[i].id if i is not None else None for i in self.active]

    def start(self):
        """ Start game and fill the board """
        self.started = True
        for i in range(12):
            self.add_card(i)
        return self.started

    def add_card(self, i, extra=False):
        """ adds new card to actives """
        if (sum([j is not None for j in self.active]) <= 12) or extra:
            # print(self.active)
            self.active[i] = self.used_cards  # simple replace
            # print(self.active)
            # print()
            if self.used_cards == 81:
                self.used_cards = None
            else:
                self.used_cards += 1
        else:
            self.active[i] = None  # remove without replace if too many
            # This solution will shift all cards on board after removed ones
            # May cause slight confusion for some players. No problem of mine ¯\_(ツ)_/¯
            # (yet)

    def add_extra(self):
        # Extend active if no set on board
        self.extra = True
        for i in range(3):
            self.add_card(i + 12, True)

    def move(self):
        for i, card in enumerate(self.active[12:]):
            if card is not None:
                self.active[self.active.index(None)] = card
                self.active[i] = None
                self.extra = False

    def validate_set(self, idxs, player=False):
        # check if cards at indices in idxs form set
        # Is called to check if set even on board, or if player clicks 3 cards.
        # If called from player, also replace card if the form set
        a, b, c = [self.deck[self.active[i]] for i in idxs]
        valid = a.is_set(b, c)
        if valid and player:
            for n in idxs:
                self.add_card(n)
            # self.move()
        return valid

    def set_on_board(self, check=False, help=False):
        # go throught every combination of cards on board to find if at least one set is on the board
        # Called by player when click on deck (blue numerated axes in corner), or if player asks for help
        cnt = sum([i is not None for i in self.active])
        for i in range(cnt):
            for j in range(i + 1, cnt):
                for k in range(j + 1, cnt):
                    if self.validate_set((i, j, k)):
                        if help:
                            return i, j, k
                        else:
                            return True
        if check:  # if called by player clicking deck and no sets on board:
            if self.extra:
                self.other_msg = ""
            else:
                self.add_extra()  # add 3 extra
        return False

    def send(self, dat):
        pkg = None
        if dat == "set_on_board?":
            pkg = self.set_on_board(help=True)

        elif dat == "no_set_on_board":
            pkg = not self.set_on_board(check=True)
            if pkg:
                self.points += 1
            else:
                self.points -= 1

        elif dat == "start":
            pkg = self.start()

        elif dat == "started?":
            pkg = self.started

        elif dat == "gimme_news":
            pkg = (81 - self.used_cards, self.get_active_ids(), {"You": self.points}, None)

        elif isinstance(dat, list):
            if len(dat) == 3:
                pkg = self.validate_set(dat, player=True)
                if pkg:
                    self.points += 1
                else:
                    self.points -= 1

        if pkg is None:
            print("\n\nSomething went terribly wrong!\n\n")
            print(dat)
        else:
            return pkg