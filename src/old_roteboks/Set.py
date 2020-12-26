import numpy as np
import matplotlib.pyplot as plt
from Card import Card, AxBorder#, number


class Game:
    def __init__(self, axs, JH=False):

        self.join = JH  # False if host, True if joining game

        if self.join:
            """
            Read from a file deck, other players, status and so on
            """
            pass
        else:
            self.deck = Card.generate_deck()
            np.random.shuffle(self.deck)
        self.active_slots = 12

        self.ax = axs
        self.used_cards = 0

        for ax in self.ax[: self.active_slots]:
            self.add_card(ax)
        self.set_on_board()
        self.numerate()

    def start(self):
        pass


    def numerate(self):
        number(self.ax[-1], 81 - self.used_cards)

    def get_card(self, ax):
        if isinstance(ax, int):
            ax = self.ax[ax]
        for child in ax.get_children():
            if isinstance(child, Card):
                return child

    def get_border(self, ax):
        if isinstance(ax, int):
            ax = self.ax[ax]
        for child in ax.get_children():
            if isinstance(child, AxBorder):
                return child

    def validate_set(self, i, j, k, replace=False):
        a = self.get_card(i)
        b = self.get_card(j)
        c = self.get_card(k)
        if a.is_set(b, c):
            if self.active_slots == 12:
                if replace:
                    for m in (i, j, k):
                        self.replace_card(m)
                    self.set_on_board()
                    self.numerate()
            else:  # if extra cards on board
                self.remove_extra_cards(i, j, k)
            return True
        else:
            return False

    def replace_card(self, i):
        self.get_card(i).remove()
        self.add_card(i)

    def set_on_board(self, help=False):
        cnt = self.active_slots
        for i in range(cnt):
            for j in range(i + 1, cnt):
                for k in range(j + 1, cnt):
                    if self.validate_set(i, j, k):
                        if help:
                            print(i, j, k)
                        return True
        print("no sets found. remove this message when dev done")
        return False

    def add_card(self, ax):
        if self.used_cards == 69:
            return 0
        if isinstance(ax, int):
            ax = self.ax[ax]
        card = self.deck[self.used_cards]
        card.make_blobs(ax)
        ax.add_artist(card)
        self.used_cards += 1

    def add_extra_cards(self):
        if self.set_on_board():
            return False  # wrongful call

        self.active_slots = 15
        for i in (12, 13, 14):
            for child in self.ax.get_children():
                if isinstance(child, AxBorder):
                    child.set_color("k")
            self.add_card(i)
        return True

    def remove_extra_cards(self, i, j, k):
        pass


class Player:
    def __init__(self, Game):
        self.clicked = []
        self.end = False
        self.points = 0
        self.penalty = 0
        self.Game = Game

    def update(self):
        if len(self.clicked) == 3:
            if self.Game.validate_set(*self.clicked, True):
                self.points += 1
                print("point given")
            else:
                self.penalty += 1
                print("PENALTY GIVEN")
            self.clicked = []
        for i in range(12):
            for child in axs[i].get_children():
                if isinstance(child, AxBorder):
                    if i in self.clicked:
                        child.set_color("r")
                    else:
                        child.set_color("k")
        plt.draw()

    def __add__(self, idx):
        if idx in self.clicked:
            self.clicked.remove(idx)
        else:
            self.clicked.append(idx)

    def add_extra(self):
        if self.Game.add_extra_cards():
            print("point given")
            self.points += 1
        else:
            print("PENALTY GIVEN")
            self.penalty += 1


def click(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click in ax
            for child in ax.get_children():  # find border colour
                if isinstance(child, AxBorder):
                    if child.get_ec() in (
                        (0, 0, 0, 1),  # if black
                        (1, 0, 0, 1),  # or if red
                    ):
                        P + i  # add click to P
                    elif child.get_ec() == (0, 1, 1, 1):
                        P.add_extra()  # click on cyan deck
    P.update()


def on_move(event):
    P.update()


def key_press(event):
    if event.key == "h":
        G.set_on_board(True)
    P.update()


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    if ax is axs[-1]:
        ax.add_artist(AxBorder(True))
    else:
        ax.add_artist(AxBorder())
    # if i < 12:  # 12 normal slots
    #     ax.add_artist(AxBorder())
    # elif i == 15:  # last, deck
    #     ax.add_artist(AxBorder(True))
    # else:  # 3 extra slots
    #     ax.add_artist(AxBorder(None))

fig.canvas.mpl_connect("button_press_event", click)
fig.canvas.mpl_connect("motion_notify_event", on_move)
fig.canvas.mpl_connect("key_press_event", key_press)

G = Game(axs)
P = Player(G)


plt.show()
