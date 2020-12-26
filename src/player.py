from network import NetworkManager
from card import Card, AxBorder
from matplotlib.offsetbox import AnchoredText
import matplotlib as mpl
import time
import numpy as np


class Player:
    """
    Class created in playSet for each player
    Is the players interaction with the game
    recieves current cards on the board from server through NetworkManager and places them on board
    """

    def __init__(self, axs, name, game):
        self.NM = NetworkManager()
        game, name, self.deck = self.NM.connect(game, name)
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
        else:  # recieve new data, print leaderboard and draw cards on board
            self.numerator, cards, table = self.NM.send("gimme_news")
            self.active = [Card(int(i) for i in id) for id in cards]
            print(self.active)
            self.draw()
            self.print(table)

    def click(self, i):
        """
        called when player clicks card
        """
        if i == 15:
            if self.active == []:  # Start game by clicking deck
                self.NM.send("start")
            elif self.NM.send("no_set_on_board"):  # claim no sets are left on board
                print("You have successfully found that there is no set on the current board.\nPoint given!")
            else:
                print("There is still at least one set on the board.\nPenalty given!")

        elif self.get_card(i) is not None:  # make sure axes actuall has card in it
            if i in self.clicked:
                self.clicked.remove(i)
                self.get_border(i).set_color("white")
            else:
                self.clicked.append(i)
                self.get_border(i).set_color("r")
        if len(self.clicked) == 3:
            if self.NM.send(self.clicked):
                print("That was a Set.\nPoint given!")
            else:
                print("That was NOT a Set.\nPenalty given!")

    def draw(self):  # draw the board (place card on board)
        i = 0  # is nessisary for before game start
        for i, card in enumerate(self.active):
            old = self.get_card(i)
            if old.is_same(card):
                continue  # dont bother replacing card with itself
            else:
                self.get_card(i).remove()
                ax = self.get_ax(i)
                card.make_blobs(ax)
                ax.add_artist(card)
                if (border := self.get_border(ax)).get_color == "r":
                    border.set_color("k")
                    self.clicked.remove(i)

        for j in range(i, 15):
            self.get_border(j).set_color("white")
            if (card := self.get_card(j)) is not None:
                card.remove()

        self.numerate(self.numerator)
        mpl.pyplot.draw()

    def print(self, table):
        " Print nice leaderboard table "
        table = {i: table[i] for i in sorted(table, key=lambda x: table[x])[::-1]}
        if table == self.table:
            return 0
        self.table = table
        out = f"\n|{'Player':^25}|{'Points':^8}|\n"
        out += "_"*len(out) + "\n"
        for plr, pts in self.table:
            out += f"|{plr:^25}|{pts:^8}|\n"
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
        print(*self.NM.send("set_on_board?"))
