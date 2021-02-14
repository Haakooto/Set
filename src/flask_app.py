import socket
from _thread import start_new_thread as SNT
from game import Game
import time
import pickle
from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "welcome"
    

"""
Server to connect players and recieve and give updates on game
"""

server = "192.168.0.15"  # set to ip of host device.
port = 5016
package_size = 2 ** 12

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    raise

s.listen()
print("Server started. Waiting for connections...")
print(f"Can be found at IP = {server}, port = {port}\n")

active_games = {}
# keys are game_ids. Values are dicts with 2 keys. "game" and "players". Last have dict with name and score as items. First is Game-instance


def thread_client(conn, name, id):
    # Threaded to keep running without halting rest of program. (parallellized)
    print(f"Established connection with '{name}' in '{id}'\n")
    while True:
        pkg = None
        data = None
        try:
            data = pickle.loads(conn.recv(package_size))

            if id in active_games:
                if data:
                    # if made it to here data will contain shit sent from player
                    # Handle different cases
                    game = active_games[id]["game"]
                    # print(game)

                    if data == "set_on_board?": # cheat
                        pkg = game.set_on_board(help=True)

                    elif data == "no_set_on_board": # claim no set on board
                        pkg = not game.set_on_board(check=True)
                        if pkg:
                            active_games[id]["players"][name] += 1
                        else:
                            active_games[id]["players"][name] -= 1

                    elif data == "start":  # start
                        pkg = game.start()

                    elif data == "started?":  # query started
                        pkg = game.started

                    elif data == "gimme_news": # update after game start. Should be most commonly called
                        pkg = (81 - game.used_cards, game.get_active_ids(), active_games[id]["players"], game.other_msg)

                    elif isinstance(data, list):  # when player has clicked 3 cards. Sends list and returns if cards form set
                        if len(data) == 3:
                            pkg = game.validate_set(data, player=True)
                            if pkg:
                                active_games[id]["players"][name] += 1
                            else:
                                active_games[id]["players"][name] -= 1

                    if pkg is None:
                        print("Weird shit. pgk is None!")
                        print("data is ", data)

                    conn.sendall(pickle.dumps(pkg))
                else:
                    break
            else:
                break
        except:
            break
    print(f"Lost connection to '{name}' in '{id}'")
    try:
        active_games[id]["players"][name + " (disconnected)"] = active_games[id]["players"].pop(name)
        active_games[id]["game"].inactive += 1
        if len(active_games[id]["players"]) == active_games[id]["game"].inactive:
            print(f"No players left in '{id}'. closing game.")
            del active_games[id]["players"]
            del active_games[id]["game"]
            del active_games[id]
    except:
        print("\nWait wHAAAT?\n")
        pass
    print()
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connetced to", addr)

    game_id, name = pickle.loads(conn.recv(package_size))
    name_taken = False
    game_already_idd = True

    if game_id is None:
        game_id = "SetGame_" + str(time.time())[-4:]
        if game_id in active_games:
            print("\nA freak event happened! Someone not specifying game_id joined game in progress!\n\n")

    if game_id in active_games:
        if (name in active_games[game_id]["players"]) or (name is None):
            name_taken = True
            name = "player " + str(len(active_games[game_id]["players"]) + 1)

        active_games[game_id]["players"][name] = 0

    else:
        print(f"Creating new game: '{game_id}'")
        if name is None:
            name = "player 1"
        game_already_idd = False
        active_games[game_id] = {}
        active_games[game_id]["players"] = {name: 0}
        active_games[game_id]["game"] = Game(game_id)

    pkg = (
        (game_already_idd, game_id),
        (name_taken, name),
    )
    conn.sendall(pickle.dumps(pkg))

    SNT(thread_client, (conn, name, game_id))  # All is ready for player to join/host a game. thread client

