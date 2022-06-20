import socket
import pickle
from .card import Card
from pynput.keyboard import Controller
import threading
import subprocess
import time


class NetworkManager:
    """
    Client-side socket-controller
    Makes connection with server
    Sends and recieves data

    """
    def __init__(self, player, server, port):
        self.player = player
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.packet_size = 2 ** 12

    def connect(self, game, name):
        """
        Players give a game_id and name they'd like when first connecting
        """
        try:
            self.client.connect(self.addr)
            return self.send((game, name))
        except socket.error as e:
            raise

    def send(self, data):
        """
        Every time player sends data, also recieve and return this to player
        """
        try:
            self.client.send(pickle.dumps(data))
            ret = self.client.recv(self.packet_size)
            if ret:
                ret = pickle.loads(ret)
            print(ret)
            if isinstance(ret, list):
                if ret[0] == "finish":
                    self.player.call_winner(ret[2])
                    self.player.active = [Card(*[int(i) for i in id]) if id is not None else None for id in ret[1]]
                    self.client.close()
                    return None

            return ret

        except:
            return None
    @classmethod
    def show_active_games(games):
        for id, game in games.items():
            print(id, time.time() - game["time"])
            for player, score in game["players"].items():
                print(f"    {player}: {score}")



class AutoUpdate(threading.Thread):
    def __init__(self, player):
        super(AutoUpdate, self).__init__()
        self.keyboard = Controller()
        self.player = player
    def run(self):
        def in_focus():
            return True
            current_window = subprocess.Popen("xdotool getwindowfocus getwindowname".split(" "), stdout=subprocess.PIPE)
            out, err = current_window.communicate()
            return out.decode("utf8") == self.player.game

        while not self.player.finished:
            if self.player.started and in_focus():
                self.keyboard.press("j")
                time.sleep(1)
                self.keyboard.release("j")
