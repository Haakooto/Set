import socket
from _thread import start_new_thread as SNT
import pickle
from board import Board


server = "192.168.1.34"
port = 5555
size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

connected = set()
board = Board()

def threaded_client(conn, name, Board):
    conn.send(pickle.dumps(deck, -1))

    while True:
        try:
            data = pickle.loads(conn.recv(size))

            if name in connected:
                if not data:
                    break
                else:
                    
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del named_games[game_name]
        print(f"Closing game {game_name}")
    except:
        print("Not sure if something wrong. look me up hehehihi")
        pass
    connected.remove(name)


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    name = "player " + str(len(connected))
    connected.add(name)

    SNT(threaded_client, (conn, name, board))
