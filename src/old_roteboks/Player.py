import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import pandas as pd

"""

Player data:
idx, int | id, int | name, str | won sets, list | status, bool
"""


fil = "game.csv"

def game_in_session():
    with open(fil, "r") as file:
        return file.read() != ""


class Player:
    def __init__(self, name=None):
        self.sets = [None, ]
        self.status = True
        self.name = str(name)
        if game_in_session():
            df = pd.read_csv(fil)
            self.id = df.at[df.shape[0] - 1, "id"] + 1
            data = {"id": self.id, "name": self.name "sets": self.sets, "status": self.status}
            df = df.append(pd.DataFrame(data))

        else:
            self.id = 0
            data = {"id": self.id, "name": self.name "sets": self.sets, "status": self.status}
            df = pd.DataFrame(data)

            # df = pd.read_csv(fil)
            # print(df)
            # print(df[df["id"] == 0])
            # print()
            # print(df.shape[0])
            # print(df[-1:])
        df.to_csv(fil, index=False)


print(pd.read_csv(fil))
Player()
print(pd.read_csv(fil))
