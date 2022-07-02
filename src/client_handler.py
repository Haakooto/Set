from _thread import start_new_thread as SNT
import pickle
import time


class ClientHandler:
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

    def point(self, game, good):
        """
        Give or take a point from player, if result is good or not
        """
        if good:
            game["players"][self.n] += 1
        else:
            game["players"][self.n] -= 1

    def loop(self):
        game = self.S.active_games[self.g]
        while self.keep_running:
            request = None  # what player sends server
            result = None   # what server replies
            try:
                request = pickle.loads(self.c.recv(self.S.ps))
                if self.g in self.S.active_games:
                    if request:
                        if request == "set_on_board?":  # cheat
                            # result = "NO CHEATING ALLOWED!"
                            result = game["game"].set_on_board(help=True)

                        elif request == "no_set_on_board":  # client claim no set
                            result = not game["game"].set_on_board(check=True)
                            self.point(game, result)
                            # if result:
                            #     game["players"][self.n] += 1
                            # else:
                            #     game["players"][self.n] -= 1

                        elif request == "start":  # command to start
                            game["timer"] = time.time()
                            result = game["game"].start()

                        elif request == "started?":  # query if game started
                            result = game["game"].started

                        elif request == "gimme_news":  # general asking for info. Called about every second
                            if not game["game"].game_over:
                                result = (game["game"].remaining(),
                                          game["game"].get_active_ids(),
                                          game["players"],
                                          game["game"].final_card_active,
                                          game["game"].other_msg,
                                          )
                            else:
                                result = ["finish",
                                          game["game"].get_active_ids(),
                                          time.time() - game["timer"],
                                          ]
                                self.keep_running = False

                        elif isinstance(request, list):  # player (maybe) found a set
                            assert len(request) == 3
                            result = game["game"].validate_set(request, player=True)
                            self.point(game, result)
                            # if result:
                            #     game["players"][self.n] += 1
                            # else:
                            #     game["players"][self.n] -= 1

                        elif isinstance(request, int):  # player guessing final card
                            id = str(request)
                            assert len(id) == 4  # int must be 4 digits long
                            result = game["game"].validate_final_card(id)
                            self.point(game, result)
                            # if result:
                            #     game["players"][self.n] += 1
                            # else:
                            #     game["players"][self.n] -= 1

                        self.c.sendall(pickle.dumps(result))
                    else:
                        break
                else:
                    break
            except:
                break
        self.S.disconnect(self)
