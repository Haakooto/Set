import matplotlib.pyplot as plt
from Card import AxBorder, Card
import numpy as np
from ast import literal_eval as Leval


class Game:
    def __init__(self, axs, name):
        self.name = name
        self.started = False
        self.path = "./datas/ongoing_game.txt"
        try:
            open(self.path, "r")
        except FileNotFoundError:
            self.init_game()

    def init_game(self):
        self.deck = Card.generate_deck()
        np.random.shuffle(self.deck)

        self.write_file()


    def write_file(self, time, ):
        """ file contains current status of game
        First line is timestamp of update start
        Second line is csv of card id
        Third line is list of active cards
            If [], game hasnt started
            Else, game will fill board with these
            On update, game clears table, and place these on board
            Update happens if current time is after timestamp
            After update, current state will be written to file in same format
        Fourth is dict of players with score
        """

    def read_file(self):
        """ see write_file for file layout """
        with open(self.path, "r") as file:
            data = file.readlines()
        time = float(data[0][:-1])
        deck = Leval(data[1][:-1])
        current = Leval(data[2][:-1])
        players = Leval(data[3][:-1])
        return time, deck, current, players



fig, axs = plt.subplots(nrows=4, ncols=4)
axs = axs.flatten()

G = Game(axs)

