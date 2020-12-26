import matplotlib.pyplot as plt
from card import AxBorder
from player import Player
import sys


cmd = sys.argv[1:]
try:
    nidx = cmd.index("-n")
    name = cmd[nidx + 1]
except:
    name = None
try:
    gidx = cmd.index("-g")
    gameid = cmd[gidx + 1]
except:
    gameid = None

"""
Use -n and -g in comandline to request name and game to join. see server.py
"""

# events to call for update
def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click on axes
            Me.click(i)
    Me.update()


def on_move_event(event):
    Me.update()


def key_press_event(event):
    if event.key == "h":  # cheat
        Me.get_if_set_on_board()
    if event.key == "r":
        print("Responsive")
    Me.update()


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    ax.add_artist(AxBorder(ax is axs[-1]))

fig.canvas.mpl_connect("button_press_event", mouse_click_event)
fig.canvas.mpl_connect("motion_notify_event", on_move_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)

Me = Player(axs, name, gameid)

plt.show()