import numpy as np
from Card import Card, AxBorder
from matplotlib.offsetbox import AnchoredText
from matplotlib.pyplot import draw as mpl_draw
import time
from datetime import datetime


class Player:
    def __init__(self, Board):
        self.B = Board
        self.B.Player = self

        self.clicked = []
        self.points = 0
        self.penalties = 0

    def click(self, i):
        if i == 15:
            if not sum(self.B.active):
                self.B.start()
            elif not self.B.set_on_board():
                self.B.add_extra()
                print("You have successfully found that there are no sets on board!\nPoint given!")
                self.points += 1
            else:
                print("There is at least one set still on board.\nPenalty given")
                self.penalties += 1
        else:
            if self.B.active[i]:
                if i in self.clicked:
                    self.clicked.remove(i)
                else:
                    self.clicked.append(i)

    def update(self):
        if len(self.clicked) == 3:
            if self.B.validate_set(*self.clicked):
                print("Point given!")
                self.points += 1
                self.B.replace(self.clicked)
