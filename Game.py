import numpy as np
from Card import Card, AxBorder
from matplotlib.offsetbox import AnchoredText
from matplotlib.pyplot import draw as mpl_draw
import time
from datetime import datetime


class Game:
    def __init__(self, axs, JH=False):
        self.join = JH

        if self.join:
            self.deck = []
            with open("crash_id.csv", "r") as file:
                ids = file.readline().split(",")
                for id in ids:
                    csfn = [int(i) for i in id]
                    self.deck.append(Card(*csfn))

        else:
            self.deck = Card.generate_deck()
            np.random.shuffle(self.deck)

        self.axs = axs
        self.active = []
        # self.used_cards = 60  # 60 used for endgame debug, 0 for actual game
        self.used_cards = 0
        self.total_cards = len(self.deck)

        self.clicked = []
        self.points = 0
        self.penalties = 0
        self.end = False
        self.last_added = False

        self.numerate()

    def get_ax(self, i):
        if isinstance(i, int):
            return self.axs[i]
        else:
            return i

    def get_card(self, ax):
        ax = self.get_ax(ax)
        for child in ax.get_children():
            if isinstance(child, Card):
                return child

    def get_border(self, ax):
        ax = self.get_ax(ax)
        for child in ax.get_children():
            if isinstance(child, AxBorder):
                return child

    def get_ax_idx(self, ax):
        for i, axi in enumerate(self.axs):
            if ax is axi:
                return i

    def empty(self, ax):
        ax = self.get_ax(ax)
        for child in ax.get_children():
            if isinstance(child, Card):
                return False
        return True

    def add_card(self, i):
        ax = self.get_ax(i)
        if self.used_cards >= 80:
            self.last_card()
            return 0
        card = self.deck[self.used_cards]
        card.make_blobs(ax)
        ax.add_artist(card)
        self.used_cards += 1
        self.active.append(self.get_ax_idx(ax))
        self.active = sorted(self.active)

    def validate_set(self, i, j, k):
        a = self.get_card(self.get_ax(i))
        b = self.get_card(self.get_ax(j))
        c = self.get_card(self.get_ax(k))
        return a.is_set(b, c)

    def replace(self, i):
        done = None
        if not isinstance(i, (tuple, list)):
            i = [i, ]
        for j in i:
            self.active.remove(j)
            self.get_card(j).remove()
        while len(self.active) < 12:
            k = 0
            while not self.empty(k):
                k += 1
            done = self.add_card(k)
            if done is not None:
                break
        while self.active[-1] > 11:
            k = 0
            while not self.empty(k):
                k += 1
            self.move(self.active[-1], k)
        if done is None:
            self.set_on_board()

    def set_on_board(self, help=False):
        cnt = len(self.active)
        for i in range(cnt):
            for j in range(i + 1, cnt):
                for k in range(j + 1, cnt):
                    if self.validate_set(i, j, k):
                        if help:
                            print(i, j, k)
                        return True
        print("no sets found. remove this message when dev done")
        if self.last_added:
            self.end_game()
        return False

    def move(self, i, j):
        to = self.get_ax(j)
        card = self.get_card(i)
        id = card._id
        card.remove()
        new = Card(*id)
        new.make_blobs(to)
        to.add_artist(new)
        self.active.remove(i)
        self.active.append(j)
        self.active = sorted(self.active)

    def numerate(self):
        ax = self.axs[-1]
        for child in ax.get_children():
            if isinstance(child, AnchoredText):
                child.remove()
        at = AnchoredText(
            str(self.total_cards - self.used_cards),
            prop=dict(size=45, weight="bold"),
            frameon=False,
            loc="center",
        )
        ax.add_artist(at)

    def click(self, i):
        if i in self.active:
            self + i

        elif i == 15:
            if self.active == []:
                self.start()
            elif not self.set_on_board():
                self.add_extra()
                print("You have successfully found that there are no sets on board.\nPoint given!")
                self.points += 1
            else:
                print("There is a set on the board.\nPENALTY GIVEN!")
                self.penalties += 1

    def add_extra(self):
        for i in (12, 13, 14):
            self.add_card(i)

    def __add__(self, i):
        if i in self.clicked:
            self.clicked.remove(i)
        else:
            self.clicked.append(i)

    def start(self):
        self.timer = time.time()
        for i in range(12):
            self.add_card(i)

    def end_game(self):
        self.end = True
        print("You finished the game!")
        print(f"Your score is {self.points - self.penalties}")
        print(f"Time spent: {time.time() - self.timer}")

    @property
    def now(self):
        return datetime.now().time()

    def update(self):
        if self.end:
            return 0
        if len(self.clicked) == 3:
            if self.validate_set(*self.clicked):
                print("point given!")
                self.points += 1
                try:
                    self.replace(self.clicked)
                except IndexError:
                    print(self.active)
                    print(self.used_cards)
                    raise
            else:
                print("PENALTY GIVEN!")
                self.penalties += 1
            self.clicked = []

        for ax in self.axs[:-1]:
            i = self.get_ax_idx(ax)
            border = self.get_border(ax)
            if i in self.active:
                if i in self.clicked:
                    border.set_color("r")
                else:
                    border.set_color("k")
            else:
                border.set_color("white")
        self.numerate()
        # print("updated at", self.now)
        mpl_draw()

    def last_card(self):
        self.last_added = True
        print("Filler function for last card.")
        print("placing on board right away")
        for i in range(12):
            ax = self.get_ax(i)
            if self.empty(ax):
                break
        card = self.deck[-1]
        card.make_blobs(ax)
        ax.add_artist(card)
        self.active.append(self.get_ax_idx(ax))
        self.active = sorted(self.active)
        self.used_cards += 1
