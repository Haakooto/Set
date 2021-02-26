import matplotlib as mpl
from matplotlib.offsetbox import AnchoredText
from datetime import timedelta

from .network import NetworkManager
from .card import Card, AxBorder
import src.sounds as sounds


class Player:
    """j
    Class created in playSet for each player
    Is the players interaction with the game
    recieves current cards on the board from server through NetworkManager and places them on board
    """

    def __init__(self, axs, server, port, name, game):

        self.NM = NetworkManager(self, server, port)
        game, name = self.NM.connect(game, name)
        valid_gid, self.game = game  # name and game_id is subject to change if not valid
        valid_name, self.name = name

        if valid_gid:
            print(f"Joined game '{self.game}'")
            if not valid_name:
                print(f"Name was already taken or not given. New name '{self.name}' given.\nYou can disconnect and reconnect with new name if you want to change. NB: will clear any points if game has already started!")
        else:
            print(f"Started new game with game id '{self.game}'")

        self.axs = axs

        self.active = []  # same list as in Game
        self.clicked = []  # clicked cards
        self.started = False
        self.numerator = 81  # cards left in deck
        self.table = ""  # Leaderboard
        self.finished = False

        self.numerate(self.numerator)  # Place '81' on deck before game starts

    def __str__(self):
        return f"Player '{self.name}' in game '{self.game}'"

    def get_ax(self, i):
        if isinstance(i, int):
            i = self.axs[i]
        return i

    def get_card(self, i):
        ax = self.get_ax(i)
        for child in ax.get_children():
            if isinstance(child, Card):
                return child

    def get_border(self, i):
        ax = self.get_ax(i)
        for child in ax.get_children():
            if isinstance(child, AxBorder):
                return child

    def update(self):
        if not self.started:  # query the server for start of game
            self.started = self.NM.send("started?")
        elif not self.finished:  # recieve new data, print leaderboard and draw cards on board
            news = self.NM.send("gimme_news")
            if news is not None:
                numerator, cards, table, other_msg = news
                if numerator is not None:
                    self.numerator = numerator
                self.active = [Card(*[int(i) for i in id]) if id is not None else None for id in cards]
                self.draw()
                table = {i: table[i] for i in sorted(table, key=lambda x: table[x])[::-1]}
                if table != self.table:
                    self.table = table
                    self.print()
                if other_msg is not None:
                    print(other_msg)
        else:
            self.draw()

    def click(self, i):
        """
        called when player clicks card
        """
        if not self.finished:
            if i == 15:
                if not self.started:  # Start game by clicking deck
                    self.started = self.NM.send("start")
                elif self.NM.send("no_set_on_board"):  # claim no sets are left on board
                    print("You have successfully found that there is no set on the current board.\nPoint given!")
                else:
                    print("There is still at least one set on the board.\nPenalty given!")
                    sounds.nelson()

            elif self.get_card(i) is not None:  # make sure axes actuall has card in it
                if i in self.clicked:
                    self.clicked.remove(i)
                else:
                    self.clicked.append(i)
            if len(self.clicked) == 3:
                if self.NM.send(self.clicked):
                    print("That was a Set.\nPoint given!")
                else:
                    print("That was NOT a Set.\nPenalty given!")
                    sounds.nelson()
                self.clicked = []
        else:
            if i in self.clicked:
                self.clicked.remove(i)
            else:
                self.clicked.append(i)
        self.update()

    def draw(self):  # draw the board (place card on board)
        for i, card in enumerate(self.active):
            if card is None:
                self.get_border(i).set_edgecolor("white")

                # syntax only valid in python3.9 (whalrus operator)
                # if (card_ := self.get_card(i)) is not None:
                    # card_.remove()

                card_ = self.get_card(i)
                if card_ is not None:
                    card_.remove()
            else:
                # if (old := self.get_card(i)) is not None:
                    # if old.is_same(card):
                old = self.get_card(i)
                if old is not None:
                    if old.is_same(card):
                        pass
                    else:
                        ax = self.get_ax(i)
                        self.get_card(ax).remove()
                        card.make_blobs(ax)
                        ax.add_artist(card)

                        if i in self.clicked:
                            self.clicked.remove(i)
                else:
                    ax = self.get_ax(i)
                    card.make_blobs(ax)
                    ax.add_artist(card)

                border = self.get_border(i)
                if i in self.clicked:
                    border.set_edgecolor("r")
                else:
                    border.set_edgecolor("k")

        self.numerate(self.numerator)
        mpl.pyplot.draw()

    def print(self, winner=False):
        " Print nice leaderboard table "
        if winner:
            out = f"\n{'Final scoreboard:':^25}|{'Points':^6}\n"
        else:
            out = f"\n{'Scoreboard':^25}|{'Points':^6}\n"
        out += "_" * 25 + "|" + "_" * 6 + "\n"
        for i, item in enumerate(self.table.items()):
            plr, pts = item
            if winner and not i:
                plr += " (WINNER!!!)"
            if plr == self.name:
                plr += " (YOU)"
            out += f"{plr:<25}|{pts:^6}\n"
        out += "\n"
        print(out)

    def numerate(self, N):
        # Say how many cards left in deck
        ax = self.axs[-1]
        for child in ax.get_children():
            if isinstance(child, AnchoredText):
                child.remove()
        at = AnchoredText(
            str(N),
            prop=dict(size=45, weight="bold"),
            frameon=False,
            loc="center",
        )
        ax.add_artist(at)

    def get_if_set_on_board(self):
        if self.started:
            reply = self.NM.send("set_on_board?")
            if not reply:
                print("No sets on board")
            else:
                print(*reply)

    def call_winner(self, time_used):
        print("\n\nNo more valid sets on board. Game is over!")
        print("Time used: ", timedelta(seconds=round(time_used)))
        self.finished = True
        self.print(True)
