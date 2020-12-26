import numpy as np
from Card import Card, AxBorder
from matplotlib.offsetbox import AnchoredText
from matplotlib.pyplot import draw as mpl_draw
import time
from datetime import datetime


class Status:
    def __init__(self, deck):
        self.deck = deck
        self.active_ids = []
        self.used_cards = 0


class Board:
    def __init__(self, axs, host=True):
        self.join = not host

        if self.join:
            print("Placeholder for multiplayer.")
            print("Not yet implemented.")
            print("Terminating.")
            from sys import exit
            exit()
        else:
            self.deck = Card.generate_deck()
            np.random.shuffle(self.deck)

        self.Stat = Status(self.deck)
        self.axs = axs

        self.active = np.zeros(len(axs), dtype=bool)
        self.used_cards = 0
        self.total_cards = len(self.deck)

        self.numerate()

    def get_ax(self, i):
        if isinstance(i, int):
            i = self.axs[i]
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
        if isinstance(ax, int):
            return ax
        for i, axes in enumerate(self.axs):
            if ax is axes:
                return i

    def empty(self, ax):
        ax = self.get_ax(ax)
        for child in ax.get_children():
            if isinstance(child, Card):
                return False
        return True

    def start(self):
        self.timer = self.time
        for i in range(12):
            self.add_card(i)

    def add_card(self, i):
        ax = self.get_ax(i)
        if self.used_cards == 80:
            self.last_card()
            return 0
        card = self.deck[self.used_cards]
        card.make_blobs(ax)
        ax.add_artist(card)
        self.used_cards += 1
        self.Stat.used_cards = self.used_cards
        self.active[self.get_ax_idx(i)] = True
        self.Stat.active_ids.append(card)

    def remove_card(self, i):
        self.active[self.get_ax_idx(i)] = False
        card = self.get_card(i)
        card.remove()
        self.Stat.active_ids.remove(card)

    def set_on_board(self, help=False):
        cnt = sum(self.active)
        for i in range(cnt):
            for j in range(i + 1, cnt):
                for k in range(j + 1, cnt):
                    if self.validate_set(i, j, k):
                        if help:
                            print(i, j, k)
                        return True
        print("No sets found. Message only for dev purposes")
        return False

    def validate_set(self, i, j, k):
        a = self.get_card(self.get_ax(i))
        b = self.get_card(self.get_ax(j))
        c = self.get_card(self.get_ax(k))
        return a.is_set(b, c)

    def add_extra(self):
        for i in (12, 13, 14):
            self.add_card(i)

    def replace(self, I):
        if "__iter__" not in dir(I):
            I = [I,]
        for i in I:



    def swap_card(self, i):
        self.used_cards += 1
        next = self.deck[self.used_cards]
