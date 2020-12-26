import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import sys
import os
import time
from Card import Card


def get_card(i):
    for child in axs[i].get_children():
        if isinstance(child, Card):
            return child


def validate_set(i, j, k):
    a = get_card(i)
    b = get_card(j)
    c = get_card(k)
    return a.is_set(b, c)


def replace_cards(i, player):
    get_card(i).remove()
    add_card(axs[i], player)


def set_on_board(help=False):
    # cards = [get_card(i) for i in range(12)]
    for i in range(12):
        for j in range(i + 1, 12):
            for k in range(j + 1, 12):
                if validate_set(i, j, k):
                    if help:
                        print(i, j, k)
                    print("validated")
                    return True
    return False


class Player:
    def __init__(self, axes):
        self.clicked = []
        self.end = False
        self.axes = axes
        self.taken = 0

    def update(self):
        if len(self.clicked) == 3:
            if validate_set(*self.clicked):
                for i in self.clicked:
                    replace_cards(i, self)
                    print(self.taken)
                if not set_on_board():
                    print("There are no sets on board")
                print("We did it")
            self.clicked = []
        for i in np.arange(12):
            if i in self.clicked:
                axs[i].get_children()[0].set_color("r")
            else:
                axs[i].get_children()[0].set_color("k")
        plt.draw()

    def __add__(self, idx):
        if idx in self.clicked:
            self.clicked.remove(idx)
        else:
            self.clicked.append(idx)


def click(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:
            P + i
    P.update()


def on_move(event):
    P.update()

def key_press(event):
    if event.key == "h":
        set_on_board(True)


def refine_ax(ax):
    ax.axis("off")
    ax.add_artist(Rectangle((0.01, 0.01), 0.98, 0.99, lw=5, fill=False, color="k"))


def add_card(ax, player):
    card = Cards[player.taken]
    card.make_blobs(ax)
    ax.add_artist(card)
    player.taken += 1


Cards = np.asarray(Card.generate())
np.random.shuffle(Cards)

fig, axs = plt.subplots(nrows=3, ncols=4)
axs = axs.flatten()

fig.canvas.mpl_connect("button_press_event", click)
fig.canvas.mpl_connect("motion_notify_event", on_move)
fig.canvas.mpl_connect("key_press_event", key_press)

P = Player(axs)

for ax in axs:
    refine_ax(ax)
    add_card(ax, P)

plt.show()

