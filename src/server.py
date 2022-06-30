import socket
import pickle
import time
import sys
from datetime import datetime

from game import Game
from client import Client

##############################
# Server file. Hosts and connects players to games
##############################
"""
Server listens for connection requests via socket
Checks if desired game is live, if not starts it
Checks if desired name is available, if not gives a new one.
Send player off to a threaded loop, Client, that lets many player interact with game simultainiously
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


# Use -s and -p in commandline to set server_IP and port to host server at

class Server:
    def __init__(self, s, p):  # starts listening for connections
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

        self.running = True

    def log(self, *args):  # prints time-stamped activity to terminal
        if len(args) == 0:
            print()
        else:
            out = f"{str(datetime.now()) :<30}"
            for arg in args:
                out += " " + str(arg)
            print(out)

    def new_connection(self, conn, addr):  # handles connection requests
        self.log("Connected to", addr)

        game_id, name = pickle.loads(conn.recv(self.ps))
        name_taken = False
        game_already_idd = True

        if not game_id:  # if not specified, make generic name
            game_id = "SetGame_" + str(time.time())[-4:]  # very unlikely to be duplicate
        elif game_id == "ListAllGames":  # return which games are in progress, and close connection
            self.log("Asked to list all games")
            conn.sendall(pickle.dumps(self.list_games()))
            self.log("Closing connection to", addr, "\n")
            conn.close()
            return

        if game_id in self.active_games:  # game exists
            if name != "Observer":
                if (name in self.active_games[game_id]["players"]) or (not name):  # if not specified, name is false
                    name_taken = bool(name)
                    name = "player " + str(len(self.active_games[game_id]["players"]) + 1)
                self.active_games[game_id]["players"][name] = 0

        else:  # start hosting new game
            self.log(f"creating new game: '{game_id}'")
            self.active_games[game_id] = {}
            self.active_games[game_id]["game"] = Game(game_id)
            self.active_games[game_id]["timer"] = 0
            game_already_idd = False

            if not name:
                name = "player 1"
            if name != "Observer":
                self.active_games[game_id]["players"] = {name: 0}

        pkg = (
            (game_already_idd, game_id),
            (name_taken, name),
        )
        conn.sendall(pickle.dumps(pkg))
        Client(self, conn, addr, name, game_id)  # start threaded loop to keep interacting with player

    def disconnect(self, client):
        self.log(f"Lost connection to '{client.n}' in '{client.g}'")
        game = self.active_games[client.g]
        game["players"][client.n + " (disconnected)"] = game["players"].pop(client.n)
        self.active_games[client.g]["game"].inactive += 1

        if len(game["players"]) == game["game"].inactive:
            self.log(f"No players left in '{client.g}'. Closing game.")
            del self.active_games[client.g]

        self.log()
        client.c.close()
        self.clients.remove(client)

    def list_games(self):
        tmp = {}
        for gname, game in self.active_games.items():
            tmp[gname] = game["players"]
        return tmp

S = Server(server, port)
while S.running:
    conn, addr = S.s.accept()
    S.new_connection(conn, addr)
