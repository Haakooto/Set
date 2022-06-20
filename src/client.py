from _thread import start_new_thread as SNT
import pickle
import time


class Client:
    def __init__(self, server, conn, addr, name, gameid):
        self.S = server
        self.c = conn
        self.a = addr
        self.n = name
        self.g = gameid
        self.keep_running = True

        self.S.log(f"Established connection with '{self.n}' in '{self.g}'\n")
        self.S.clients.append(self)
        SNT(self.loop, ())

    def __repr__(self):
        return f"Player '{self.n}' in game '{self.g} at {self.a}"

    def __hash__(self):
        return hash(self.n + self.g + self.a)

    def loop(self):
        game = self.S.active_games[self.g]
        while self.keep_running:
            pkg = None
            data = None
            try:
                data = pickle.loads(self.c.recv(self.S.ps))
                if self.g in self.S.active_games:
                    if data:
                        if data == "set_on_board?":  # cheat
                            pkg = "NO CHEATING ALLOWED!"
                            # pkg = game.set_on_board(help=True)

                        elif data == "no_set_on_board":  # client claim no set
                            pkg = not game["game"].set_on_board(check=True)
                            if pkg:
                                game["players"][self.n] += 1
                            else:
                                game["players"][self.n] -= 1

                        elif data == "start":
                            game["timer"] = time.time()
                            pkg = game["game"].start()

                        elif data == "started?":
                            pkg = game["game"].started

                        elif data == "gimme_news":
                            if not game["game"].game_over:
                                pkg = (game["game"].remaining(), game["game"].get_active_ids(), game["players"], game["game"].other_msg)
                            else:
                                pkg = ["finish", game["game"].get_active_ids(), time.time() - game["timer"]]
                                self.keep_running = False

                        elif isinstance(data, list):
                            assert len(data) == 3
                            pkg = game["game"].validate_set(data, player=True)
                            if pkg:
                                game["players"][self.n] += 1
                            else:
                                game["players"][self.n] -= 1
                        self.c.sendall(pickle.dumps(pkg))
                    else:
                        break
                else:
                    break
            except:
                break
        self.S.disconnect(self)
