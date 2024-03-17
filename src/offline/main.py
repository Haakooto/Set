import matplotlib.pyplot as plt
from card import AxBorder
from game import Game
from player import Player
import sys


# events to call for update
def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click on axes
            Me.click(i)
    Me.update()


def on_move_event(event):
    Me.update()
    # pass

def key_press_event(event):
    if event.key == "h":  # cheat
        Me.get_if_set_on_board()
    if event.key == "r":
        print("Responsive")
    if event.key == "g":
        plt.close()
    if event.key == "i":
        print(Board.active)
    Me.update()


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    ax.add_artist(AxBorder(ax is axs[-1]))


fig.canvas.mpl_connect("button_press_event", mouse_click_event)
fig.canvas.mpl_connect("motion_notify_event", on_move_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)


Board = Game()
Me = Player(axs, Board)
Me.update()

plt.show()