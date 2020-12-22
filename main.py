# import numpy as np
import matplotlib.pyplot as plt
from Card import AxBorder, Card
from Game import Game


def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click in ax
            Game.click(i)
    Game.update()


def on_move_event(event):
    Game.update()


def key_press_event(event):
    if event.key == "h":
        Game.set_on_board(help=True)
    if event.key == "r":
        print("Responsive")
    Game.update()


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    if ax is axs[-1]:
        ax.add_artist(AxBorder(True))
    else:
        ax.add_artist(AxBorder())

fig.canvas.mpl_connect("button_press_event", mouse_click_event)
fig.canvas.mpl_connect("motion_notify_event", on_move_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)

Game = Game(axs)
with open("id_backup.csv", "w") as file:
    lst = Card.id_list(Game.deck)
    file.write(lst[0])
    for id in lst[1:]:
        file.write(f",{id}")

plt.show()
