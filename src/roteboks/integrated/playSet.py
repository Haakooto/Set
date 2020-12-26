import matplotlib as plt
from card import AxBorder
from board import Board
from player import Player
from network import Manager
import pickle
import sys


def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:
            P.click(i)
    P.update()
    B.update()


def on_move_event(event):
    P.update()
    B.update()


def key_press_event(event):
    if event.key == "h":
        Board.set_on_board(help=True)
    if event.key == "r":
        print("Responsive")
    P.update()
    B.update()


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    ax.add_artist(AxBorder(ax is axs[-1]))

fig.canvas.mpl_connect("button_press_event", mouse_click_event)
fig.canvas.mpl_connect("motion_notify_event", on_move_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)


B = Board(axs, Manager())
P = Player(B)

plt.show()