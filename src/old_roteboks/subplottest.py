import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import matplotlib as mpl


class Slot(mpl.axes.Axes):
    def __init__(self, ax, active=True, ):
        self = ax

    def lololo(self):
        print("it worked")

fig, ax = plt.subplots()

ax = TestAx(ax)
print(type(ax))
