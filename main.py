import matplotlib.pyplot as plt
from threading import Thread
import subprocess
import socket
from pynput.keyboard import Controller

import sys
import time

from src.card import AxBorder
from src.player import Player
from src.network import AutoUpdate


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
if "-l" in cmd:
    name = None
elif "-i" in cmd:
    game = None

"""
Use -n and -g in commandline to request name and game to join. see server.py
Use -s and -p in commandline to set server_IP and port to search for server at
Use -l  or -i in commandline to list active games or inquire in server
"""


# events to call for update
def mouse_click_event(event):
    for i, ax in enumerate(axs):
        if ax.contains(event)[0]:  # if click on axes
            Me.click(i)
    Me.update()


def on_move_event(event):
    # Me.update()
    pass


def key_press_event(event):
    if event.key == "h":  # cheat
        Me.get_if_set_on_board()
    if event.key == "r":
        print("Responsive")
    if event.key == "q":
        Me.finished = True
    if event.key == "g":
        # reserved for testing
        pass
    if event.key == "j":
        # reserved for autoclicker
        pass
    Me.update()


def say(name):
    """
    Start of chat system to be implemented later
    """
    while True:
        a = input()
        print(a)


def auto_click(player):
    while not player.started:
        time.sleep(0.1)

    keyboard = Controller()
    while not (player.finished and player.started):
        current_window = subprocess.Popen("xdotool getwindowfocus getwindowname".split(" "), stdout=subprocess.PIPE)
        out, err = current_window.communicate()
        if out.decode("utf8") == player.game:
            keyboard.press("j")
            time.sleep(0.01)
            keyboard.release("j")
            time.sleep(1)
        if player.finished:
            break


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
fig.canvas.mpl_connect("motion_notify_event", on_move_event)
fig.canvas.mpl_connect("key_press_event", key_press_event)

Me = Player(axs, server, port, name, gameid)
if Me.server_stop:
    plt.clf()
    sys.exit(0)

plt.get_current_fig_manager().set_window_title(Me.game)
Me.update()


# talker = Thread(target=say, args=(Me.name,))
# clicker = Thread(target=auto_click, args=(Me,))
# talker.start()
# clicker.start()

# clicker = AutoUpdate(Me)
# clicker.start()

plt.show()

# clicker.join()
# talker.join(timeout=1)
# clicker.join(timeout=1)