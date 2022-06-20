import socket
from _thread import start_new_thread as SNT
import pickle

import time
import sys
from datetime import datetime

from game import Game


def server_log(*args):
    if len(args) == 0:
        print()
    else:
        out = f"{str(datetime.now()) :<30}"
        for arg in args:
            out += " " + str(arg)
        print(out)

"""
Server to connect players and recieve and give updates on game
"""

cmd = sys.argv[1:]
try:
    port = int(cmd[cmd.index("-p") + 1])
except:
    port = 5016
try:
    server = cmd[cmd.index("-s") + 1]
except:
    server = socket.gethostname()

"""
Use -s and -p in commandline to set server_IP and port to host server at
"""

package_size = 2 ** 12
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error:
    raise

s.listen()
server_log("Server started. Waiting for connections...")
server_log(f"Can be found at IP = {server}, port = {port}\n")

active_games = {}
# keys are game_ids. Values are dicts with 2 keys. "game" and "players". Last have dict with name and score as items. First is Game-instance


def thread_client(conn, name, id):
    # Threaded to keep running without halting rest of program. (parallellized)
    server_log(f"Established connection with '{name}' in '{id}'\n")
    game_finished = False
    while not game_finished:
        pkg = None
        data = None
        try:
            data = pickle.loads(conn.recv(package_size))

            if id in active_games:
                if data:
                    # if made it to here data will contain shit sent from player
                    # Handle different cases
                    game = active_games[id]["game"]

                    if data == "set_on_board?": # cheat
                        pkg = game.set_on_board(help=True)

                    elif data == "no_set_on_board": # claim no set on board
                        pkg = not game.set_on_board(check=True)
                        if pkg:
                            active_games[id]["players"][name] += 1
                        else:
                            active_games[id]["players"][name] -= 1

                    elif data == "start":  # start
                        active_games[id]["timer"] = time.time()
                        pkg = game.start()

                    elif data == "started?":  # query started
                        pkg = game.started

                    elif data == "gimme_news": # update after game start. Should be most commonly called
                        if not game.game_over:
                            pkg = (game.remaining(), game.get_active_ids(), active_games[id]["players"], game.other_msg)
                        else:
                            pkg = ["finish", game.get_active_ids(), time.time() - active_games[id]["timer"]]
                            game_finished = True

                    elif isinstance(data, list):  # when player has clicked 3 cards. Sends list and returns if cards form set
                        if len(data) == 3:
                            pkg = game.validate_set(data, player=True)
                            if pkg:
                                active_games[id]["players"][name] += 1
                            else:
                                active_games[id]["players"][name] -= 1

                    if pkg is None:
                        server_log("Weird shit. pgk is None!")
                        server_log("data is ", data)

                    conn.sendall(pickle.dumps(pkg))
                else:
                    break
            else:
                break
        except:
            break
    server_log(f"Lost connection to '{name}' in '{id}'")
    try:
        active_games[id]["players"][name + " (disconnected)"] = active_games[id]["players"].pop(name)
        active_games[id]["game"].inactive += 1
        if len(active_games[id]["players"]) == active_games[id]["game"].inactive:
            server_log(f"No players left in '{id}'. closing game.")
            del active_games[id]["players"]
            del active_games[id]["game"]
            del active_games[id]
    except:
        server_log("\nWait wHAAAT?\n")
        pass
    server_log()
    conn.close()


def connect_client(game_id, name, conn):
    name_taken = False
    game_already_idd = True

    # Start new game
    if game_id == "":
        game_id = "SetGame_" + str(time.time())[-4:]
        if game_id in active_games:
            server_log("A freak event happened! Someone not specifying game_id joined game in progress!")

    # Join existing game
    if game_id in active_games:
        if (name in active_games[game_id]["players"]) or (name == ""):
            if name != "":
                name_taken = True
            name = "player " + str(len(active_games[game_id]["players"]) + 1)

        active_games[game_id]["players"][name] = 0  # initialize player with score

    else: # Join new game
        server_log(f"Creating new game: '{game_id}'")
        if name == "":
            name = "player 1"
        game_already_idd = False
        active_games[game_id] = {}
        active_games[game_id]["players"] = {name: 0}
        active_games[game_id]["game"] = Game(game_id)
        active_games[game_id]["timer"] = 0

    pkg = (
        (game_already_idd, game_id),
        (name_taken, name),
    )
    conn.sendall(pickle.dumps(pkg))

    SNT(thread_client, (conn, name, game_id))  # All is ready for player to join/host a game. thread client


while True:
    conn, addr = s.accept()
    server_log("Connetced to", addr)

    game_id, name = pickle.loads(conn.recv(package_size))
    print(game_id, name)
    if isinstance(game_id, str) and isinstance(name, str):
        connect_client(game_id, name, conn)

    elif isinstance(game_id, str):
        if game_id in active_games:
            server_log("Sending status in ", game_id)
            conn.sendall(pickle.dumps(({game_id: active_games[game_id]}, None)))
        else:
            server_log("Sending active games")
            conn.sendall(pickle.dumps((active_games, None)))
