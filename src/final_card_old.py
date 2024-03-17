import matplotlib.pyplot as plt
from matplotlib.offsetbox import DrawingArea, AnchoredText
from matplotlib.transforms import Affine2D
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import sys
from copy import copy
import numpy as np
from card import Card, AxBorder


def add_subplot_axes(ax, rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]
    subax = fig.add_axes([x, y, width, height])
    return subax


class FinalCard(Card):
    def __init__(self, ax, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ax = ax
        self.c = 1
        self.s = 1
        self.f = 1
        self.n = 1

        self.cover()

    def cover(self):
        # self.ax = ax
        x = [(i + 1) * 0.07 + i * 0.24 for i in range(3)]
        y = [(i + 1) * 0.04 + i * 0.20 for i in range(4)][::-1]
        x, y = np.meshgrid(x, y)
        positions = list(zip(x.flatten(), y.flatten()))
        self.slots = [add_subplot_axes(self.ax, [*p, 0.24, 0.20]) for p in positions]

        cards = [Card(i, 0, 3, 1) for i in range(1, 4)]
        cards += [Card(0, i, 3, 1) for i in range(1, 4)]
        cards += [Card(0, 0, i, 1) for i in range(1, 4)]
        cards += [Card(0, 0, 3, i) for i in range(1, 4)]
        for i, slot in enumerate(self.slots):
            slot.axis("off")
            slot.add_artist(AxBorder(ec="k"))
            card = cards[i]
            card.make_blobs(slot)
            slot.add_artist(card)


    def cover(self):
        dd = 0.04

        x = [(i + 1) * dd + i * (1 - 5 * dd) / 4 for i in range(4)]
        y = 1 - dd - 0.12

        self.specifiers = [add_subplot_axes(self.ax, [i, y, 0.18, 0.12]) for i in x]
        self.confirm = add_subplot_axes(self.ax, (dd, dd, 1 - 2 * dd, 0.12))
        self.display = add_subplot_axes(self.ax, (dd, 0.12 + 2 * dd, 1 - 2 * dd, 1 - 2 * 0.12 - 4 * dd))
        self.sub_axes = self.specifiers + [self.confirm, self.display]

        for ax in self.sub_axes:
            ax.axis("off")
            ax.add_artist(AxBorder(ec="k"))

        C = Card(3,3,3,3)
        C.make_blobs(self.display)
        self.display.add_artist(C)




    def uncover(self, ax):
        # Maybe do the check here?
        for child in ax.get_children():
            # go through and remove all minicards
            pass

        self.make_blobs(ax)



def final_card():
    fig, axs = plt.subplots(nrows=4, ncols=4)
    axs = axs.flatten()
    for ax in axs:
        ax.axis("off")
        ax.add_artist(AxBorder(ec="k"))

    F = FinalCard(axs[0], 0, 0, 1, 1)
    # F.cover(axs[0])

    C = Card(2,2,2,2)
    C.make_blobs(axs[1])
    axs[1].add_artist(C)




    plt.show()

if __name__ == "__main__":
    final_card()