import matplotlib.pyplot as plt
from card import AxBorder
from player import Player
import sys
from threading import Thread, Lock


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
try:
    pidx = cmd.index("-p")
    port = int(cmd[pidx + 1])
except:
    port = 5016
try:
    sidx = cmd.index("-s")
    server = cmd[sidx + 1]
except:
    server = "192.168.0.15"

"""
Use -n and -g in commandline to request name and game to join. see server.py
Use -s and -p in commandline to set server_IP and port to search for server at
"""


# events to call for update
def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click on axes
            Me.click(i)
    Me.update()


def on_move_event(event):
    Me.update()
    pass


def key_press_event(event):
    if event.key == "h":  # cheat
        Me.get_if_set_on_board()
    if event.key == "r":
        print("Responsive")
    if event.key == "g":
        print(Me.active)
        # plt.close()
    Me.update()


def say(name):
    """
    Start of chat system to be implemented later
    """
    while True:
        a = input()
        print(a)


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    ax.add_artist(AxBorder(ax is axs[-1]))

fig.canvas.mpl_connect("button_press_event", mouse_click_event)
fig.canvas.mpl_connect("motion_notify_event", on_move_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)

Me = Player(axs, server, port, name, gameid)
Me.update()

# talker = Thread(target=say, args=(Me.name,))
# talker.start()

plt.show()
# talker.join(timeout=1)
