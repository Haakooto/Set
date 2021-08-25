import socket
from _thread import start_new_thread as SNT
import pickle
import time
import sys
from datetime import datetime

from game import Game
from client import Client

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


class Server:
    def __init__(self, s, p):
        self.ps = 2 ** 12  # package_size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((s, p))
        except socket.error:
            raise

        self.s.listen(5)
        self.log("Server started. Waiting for connections...")
        self.log(f"Can be found at IP = {s}, port = {p}\n")

        self.active_games = {}
        self.clients = []

        SNT(self.do, ())

    def log(self, *args):
        if len(args) == 0:
            print()
        else:
            out = f"{str(datetime.now()) :<30}"
            for arg in args:
                out += " " + str(arg)
            print(out)

    def do(self):
        safe_words = "quit q exit end stop fuckoff die".split()
        while True:
            i = input()
            if i in safe_words:
                self.shut_down()
            else:
                exec(i)

    def new_connection(self, conn, addr):
        self.log("Connected to", addr)

        game_id, name = pickle.loads(conn.recv(self.ps))
        print(name, type(name))
        name_taken = False
        game_already_idd = True

        if game_id is None:
            game_id = "SetGame_" + str(time.time())[-4:]
        elif game_id == "ListAllGames":
            conn.sendall(pickle.dumps(self.active_games))
            return

        if game_id in self.active_games:
            if name != "Observer":
                if (name in self.active_games[game_id]["players"]) or (name is None):
                    if name is not None:
                        name_taken = True
                    name = "player " + str(len(self.active_games[game_id]["players"]) + 1)
                self.active_games[game_id]["players"][name] = 0

        else:
            self.log(f"creating new game: '{game_id}'")
            self.active_games[game_id] = {}
            self.active_games[game_id]["game"] = Game(game_id)
            self.active_games[game_id]["timer"] = 0
            game_already_idd = False

            if name is None:
                name = "player 1"
                # self.active_games[game_id]["players"] = {"player 1": 0}
            if name != "Observer":
                self.active_games[game_id]["players"] = {name: 0}

        pkg = (
            (game_already_idd, game_id),
            (name_taken, name),
        )
        conn.sendall(pickle.dumps(pkg))
        Client(self, conn, addr, name, game_id)

    def disconnect(self, client):
        self.log(f"Lost connection to '{client.n}' in '{client.g}'")
        game = self.active_games[client.g]
        game["players"][client.n + " (disconnected)"] = game["players"].pop(client.n)
        self.active_games[client.g]["game"].inactive += 1

        if len(game["players"]) == game["game"].inactive:
            self.log(f"No players left in '{client.g}'. Closing game.")
            del game["players"]
            del game["game"]
            del game
        self.log()
        client.c.close()
        self.clients.remove(client)

    def shut_down(self):
        print("lol")
        pass


S = Server(server, port)
while True:
    conn, addr = S.s.accept()
    S.new_connection(conn, addr)
