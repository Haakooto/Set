import socket
import pickle
from threading import Thread
import time
from .card import Card


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
            if isinstance(ret, list):
                if ret[0] == "finish":
                    self.player.call_winner(ret[2])
                    self.player.active = [Card(*[int(i) for i in id]) if id is not None else None for id in ret[1]]
                    self.client.close()
                    return None

            return ret

        except:
            print("Connetion to server lost")
            self.client.close()
            return None


class AutoUpdate:
    def __init__(self, player, f):
        self.key = "j"
        self.player = player
        self.updater = Thread(target=self.update, args=(f,))
        self.updater.start()

    def update(self, f):
        while not self.player.finished:
            f(self)
            time.sleep(1)