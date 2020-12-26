import matplotlib.pyplot as plt
from matplotlib.offsetbox import DrawingArea
from matplotlib.transforms import Affine2D
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import sys
from copy import copy
import numpy as np

Path = mpath.Path


class AxBorder(mpatches.Rectangle):
    """ Class making it easier to use border """

    def __init__(self, last=False):
        c = (0.01, 0.01)
        super().__init__(c, 0.98, 0.99, lw=5, fill=False, ec="white")
        if last:
            self.set_fill(False)
            self.set_color("cyan")
            self.set_hatch("x+O")


class Card(DrawingArea):
    def __init__(self, colour, shape, fill, number):
        super().__init__(1, 1, 0, 0)  # init unit-size DrawingArea
        """
        Colours: 1: green
                 2: purple / blue
                 3: red
        Shapes:  1: ellipse
                 2: rombus
                 3: arrow
        Fills:   1: no
                 2: sparse
                 3: dense
        Number:  1: one
                 2: two
                 3: three
        """

        self.c = colour
        self.s = shape
        self.f = fill
        self.n = number

        self.id = f"{self.c}{self.s}{self.f}{self.n}"
        self._id = np.asarray([int(i) for i in self.id])

        # Dicts to relate values to readable descriptions
        self.cd = {1: "green", 2: "blue", 3: "red"}
        self.sd = {1: "ellipse", 2: "rombus", 3: "arrow"}
        self.fd = {1: "none", 2: "hatched", 3: "filled"}
        self.nd = {1: "one", 2: "two", 3: "three"}

    def __str__(self):
        c = self.cd[self.c]
        s = self.sd[self.s]
        f = self.fd[self.f]
        n = self.nd[self.n]
        return f"colour: {c}, shape: {s}, fill: {f}, number: {n}"

    def __repr__(self):
        return f"<Set.Card.Card object {self.id}>"

    def is_set(self, this, that):
        """
        Value for each category is labeled 1,2,3
        Sum of values of one category of three cards
        is divisible by 3 only if all are equal or unequal
        if all category sums are divisible by three
        the mod of all separately is 0.

        ._id is array with each category, so mod work elementwise
        sum is 0 is self, this and that form set
        """
        ids = self._id + this._id + that._id
        isset = sum(ids % 3)
        return not isset

    def make_blobs(self, ax):
        # Takes in axes-object to transform correctly within axes

        patches = []
        if self.s == 1:  # Ellipse
            patch = mpatches.Ellipse((0.5, 0.5), 0.7, 0.2)
        elif self.s == 2:  # Rombus
            data = [
                (Path.MOVETO, [0.5, 0.6]),
                (Path.LINETO, [0.15, 0.5]),
                (Path.LINETO, [0.5, 0.4]),
                (Path.LINETO, [0.85, 0.5]),
                (Path.LINETO, [0.5, 0.6]),
            ]
            codes, verts = zip(*data)
            path = Path(verts, codes)
            patch = mpatches.PathPatch(path)

        elif self.s == 3:  # Arrow
            data = [  # Can make any shape, just set coords in unit axes
                (Path.MOVETO, [0.15, 0.55]),
                (Path.LINETO, [0.15, 0.45]),
                (Path.LINETO, [0.65, 0.45]),
                (Path.LINETO, [0.6, 0.35]),
                (Path.LINETO, [0.85, 0.5]),
                (Path.LINETO, [0.6, 0.65]),
                (Path.LINETO, [0.65, 0.55]),
                (Path.LINETO, [0.15, 0.55]),
            ]
            codes, verts = zip(*data)
            path = Path(verts, codes)
            patch = mpatches.PathPatch(path)

        patch.set_linewidth(5)
        patch.set_color(self.cd[self.c])

        if self.f == 1:
            patch.set_fill(False)
        elif self.f == 2:
            patch.set_fill(False)
            patch.set_hatch("x++")
            # style of shading. See mpl patch documentation
        elif self.f == 3:
            patch.set_fill(True)

        patches.append(patch)
        patches[0].set_transform(ax.transData)

        # add one or two more, and place them nicely
        if self.n == 2:
            patches.append(copy(patch))
            up = Affine2D().translate(0, 0.2)
            down = Affine2D().translate(0, -0.2)
            patches[0].set_transform(up + ax.transData)
            patches[1].set_transform(down + ax.transData)
        elif self.n == 3:
            patches.append(copy(patch))
            patches.append(copy(patch))
            up = Affine2D().translate(0, 0.3)
            down = Affine2D().translate(0, -0.3)
            rot = Affine2D().rotate_deg_around(0.5, 0.5, 180)
            # Middle one is rotated. Effect only visible for non-symmetric arrow
            patches[0].set_transform(up + ax.transData)
            patches[1].set_transform(down + ax.transData)
            patches[2].set_transform(rot + ax.transData)

        for patch in patches:
            self.add_artist(patch)

    @staticmethod
    def generate_deck():
        """ Non-shuffled(!) full deck """
        deck = []
        for c in range(1, 4):
            for s in range(1, 4):
                for f in range(1, 4):
                    for n in range(1, 4):
                        deck.append(Card(c, s, f, n))
        return deck

    @staticmethod
    def id_list(deck):

        ids = []
        for card in deck:
            ids.append(card.id)
        return ids


if __name__ == "__main__":
    fig, ax = plt.subplots()
    try:
        A = sys.argv[1]
        C = Card(*[int(i) for i in A])
    except:
        C = Card(1, 1, 1, 1)
    C.make_blobs(ax)
    ax.add_artist(C)
    plt.show()
