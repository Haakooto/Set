import matplotlib.pyplot as plt
import socket
import sys

from src.card import AxBorder
from src.player import Player, Observer
from src.network import NetworkManager, AutoUpdate


cmd = sys.argv[1:]
try:
    nidx = cmd.index("-n")
    name = cmd[nidx + 1]
except:
    name = ""
try:
    gidx = cmd.index("-g")
    gameid = cmd[gidx + 1]
except:
    gameid = ""
try:
    pidx = cmd.index("-p")
    port = int(cmd[pidx + 1])
except:
    port = 5016
try:
    sidx = cmd.index("-s")
    server = cmd[sidx + 1]
except:
    server = socket.gethostname()

if "-l" in cmd or gameid == "ListAllGames":
    NetworkManager(None, server, port, list_games=True)
    sys.exit()
elif "-o" in cmd:
    name = "Observer"

"""
Use -n and -g in commandline to request name and game to join. see server.py
Use -s and -p in commandline to set server_IP and port to search for server at
Use -l  or -o in commandline to list active games, or start observe mode
"""


# events to call for update
def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click on axes
            Me.click(i)
    Me.update()


def key_press_event(event):
    if   event.key == "h": Me.get_if_set_on_board()  # cheating
    elif event.key == "r": print("Responsive")
    elif event.key == "q": Me.finish()
    elif event.key == "g": pass  # reserved for testing
    elif event.key == "j": pass  # reserved for autoclicker
    Me.update()


fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()
for ax in axs:
    ax.axis("off")
    ax.final_card = False
    ax.add_artist(AxBorder(ax is axs[-1]))

plt.subplots_adjust(left=0.01,
                    bottom=0.01,
                    right=0.99,
                    top=0.99,
                    wspace=0.1,
                    hspace=0.1)

fig.canvas.mpl_connect("button_press_event", mouse_click_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)

if name == "Observer":  # ! not implemented
    Me = Observer(axs, server, port, name, gameid)
else:
    Me = Player(axs, server, port, name, gameid)
Me.update()
AutoUpdate(Me, key_press_event)

plt.show()
