import socket
import pickle
from matplotlib.pyplot import close


class NetworkManager:
    """
    Player-side controller of network shit.
    Makes connection with server
    Sends and recieves data

    Currently only works for servers and players on same network. Figure out how to make online
    Set server IP to relevant shit.
    Port 5555 should be default
    Change port when its taken
    ServerIP and port must be same as in server.py
    """
    def __init__(self, server, port):
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
                return pickle.loads(ret)
        except:
            close()
