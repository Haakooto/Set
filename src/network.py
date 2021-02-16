import socket
import pickle
from matplotlib.pyplot import close


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
                    self.player.call_winner(ret[1])
                    close()
                    self.client.close()
                    return None

            return ret

        except:
            print("Connetion to server lost")
            close()
            self.client.close()
            return None
