import socket
import pickle


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
    def __init__(self, server="192.168.1.34", port=5558):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.packet_size = 2048

    def connect(self, game, name):
        """
        Players give a game_id and name they'd like when first connecting
        """
        try:
            self.client.connect(self.addr)
            return self.send((game, name))
        except socket.error as e:
            print(e)

    def send(self, data):
        """
        Every time player sends data, also recieve and return this to player
        """
        try:
            self.client.send(pickle.dumps(data))
            ret = self.client.recv(self.packet_size)
            if ret:
                return pickle.loads(ret)
            # print(ret)
            # print(pickle.loads(ret))
            # return pickle.loads(self.client.recv(self.packet_size))  # Ideally only this line if needed after 'self.client.send...'
            # # But because of problems, different things have been tried. (This is the location of the bug. And not nessisarily the cause of said bug)
        except socket.error as e:
            print("\n\nThere was an error in sending/recieving from server")
            print(e)