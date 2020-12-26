import socket
import pickle


class Manager:
    def __inti__(self, server="192.168.1.34", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.size = 4096  # size of sending and recieving packages

        def connect(self):
            try:
                self.client.connect(self.addr)
                return self.client.recv(self.size).decode()
            except:
                print("Could not connect to server.")
                pass

        def send(self, data):
            try:
                self.client.send(pickle.dumps(data, -1))
                return pickle.loads(self.client.recv(self.size))
            except socket.error as e:
                print(e)