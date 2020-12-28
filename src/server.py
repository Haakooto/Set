import socket
from _thread import start_new_thread as SNT
from game import Game
# from card import Card
import time
import pickle


"""
Server to connect players and recieve and give updates on game
Mostly ripped off from https://www.youtube.com/watch?v=McoDjOCb2Zo (theres a github to find the code)
(Havent exteded for real online. will only work for devices on same network)
"""

server = "192.168.1.34"  # set to ip of host device. Must be same as in network.py
port = 5555  # 5555 should be free. increase by 1 when its not (stop this file with ctrl+c NOT ctrl+d. will not free port properly)
package_size = 2 ** 12

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    raise

s.listen()
print("Server started. Waiting for connections...\n")

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
        del active_games[id]["players"][name]
        if not len(active_games[id]["players"]):
            print(f"No players left in '{id}'. closing game.")
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

