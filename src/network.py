import socket
import pickle
import threading
import time
from .card import Card


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
                    self.player.draw()
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
    """
    Automatically interacts with game to trigger updates by calling key_press_event()
    """
    def __init__(self, player, kpe):  # kpe: key_press_event
        self.key = "j"
        self.rate = .1  # refresh rate
        self.player = player
        self.player.AU = self

        # threading.excepthook = lambda arg: print(f"the thing happened: {arg.exc_value}")

        self.updater = threading.Thread(target=self.update, args=(kpe,))
        self.updater.start()

    def update(self, kpe):
        while not self.player.finished:
            kpe(self)
            time.sleep(self.rate)
