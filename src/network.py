import socket
import pickle
from threading import Thread
import time
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
    def __init__(self, player, server, port, list_games=False):
        self.player = player
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.packet_size = 2 ** 12

        if list_games:
            self.list_games()

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
            if ret == "byebye":
                self.player.AU.halt()
            if isinstance(ret, list):
                if ret[0] == "finish":
                    self.player.call_winner(ret[2])
                    self.player.active = [Card(*[int(i) for i in id]) if id is not None else None for id in ret[1]]
                    self.client.close()
                    return None

            return ret

        except:
            return None

    def list_games(self):
        data = self.connect("ListAllGames", None)
        # TODO:  format this nicely
        print(data)


class AutoUpdate:
    def __init__(self, player, kpe):
        self.key = "j"
        self.rate = 1  # refresh rate
        self.player = player
        self.player.AU = self

        self.updater = Thread(target=self.update, args=(kpe,))
        self.updater.start()

    def update(self, kpe):
        while not self.player.finished:
            kpe(self)
            time.sleep(self.rate)
