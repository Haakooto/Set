import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from matplotlib.offsetbox import DrawingArea, AnchoredOffsetbox
from matplotlib.patches import Circle, Rectangle, CirclePolygon
# from myplotlib import DrawingArea

class Game(AnchoredOffsetbox):
    def __init__(self, w, h, *args, **kwargs):
        self.w = w
        self.h = h
        self.area = DrawingArea(w, h, 0, 0)
        super().__init__(loc="center", pad=0, borderpad=0,
                        child=self.area, prop=None, frameon=True)

    def __add__(self, artist):
        self.area.add_artist(artist)


# class Slot(Rectangle):
#     def __init__(self, DA, xy, *args, **kwargs):
#         self.area = Game(10, 10, 0, 0)
#         x, y = xy
#         x *= DA.w
#         y *= DA.h

#         w = 15
#         h = 20

#         super().__init__((x, y), w, h, angle=np.pi/4, fill=False,  *args, **kwargs)
#         DA + self


# Board = AnchoredOffsetbox("center", frameon=True)
# Board = Game(100, 100, 40, 0)
# Board.set_child(DrawingArea(100,100,0,0))
# Board._child.add_artist(Rectangle((0, 0), 100, 10))

R1 = Rectangle((0.5, 0.5), 50, 50)
DA = DrawingArea(100, 100, 0, 0)
DA.add_artist(R1)
# print(DA.get_offset())
DA.set_offset((4, 4))
# print(DA.get_transform())

class Card:
    def __init__(self, c, s, f, n):
        """
        Colours: 1: green
                 2: purple / blue
                 3: red
        Shapes:  1: circle
                 2: diamond
                 3: blob
        Fills:   1: no
                 2: sparse
                 3: dense
        Number:  1: one
                 2: two
                 3: three
        """
        self.c = c  # colour
        self.s = s  # shape
        self.f = f  # fill
        self.n = n  # number

def click(event):
    x, y = fig.transFigure.transform((event.x, event.y))
    print(x, "  ", y)

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
fig.canvas.mpl_connect("button_press_event", click)

# Board = Game(200, 200, 0, 0)
# Board + Slot(Board, (0.5, 0.5))
# Board + Slot(Board, (0.5, 0.3))
ax.add_artist(DA)

plt.show()

