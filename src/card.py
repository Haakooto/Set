import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import DrawingArea
from matplotlib.transforms import Affine2D
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from copy import copy
import sys

Path = mpath.Path
Patch = mpatches.PathPatch


class AxBorder(mpatches.Rectangle):
    """
    Rectangle-object around each Axes.
    If Axes for card, only border is visible and changes colour.
    If Axes for deck (last); is hatched and beautiful
    """

    def __init__(self, last=False, ec="white"):
        c = (0.01, 0.01)
        super().__init__(c, 0.98, 0.99, lw=5, fill=False, ec=ec)
        if last:
            self.set_fill(False)
            self.set_color("cyan")
            self.set_hatch("x+O")


class Card(DrawingArea):
    """
    Drawable cards with relevant properties

    The current possible values for the properties are not nessisarily final,
    However, as its only for visualization changes are faaaar down on the priority list
    """

    Rectangle = mpatches.Rectangle((0.25, 0.4), 0.5, 0.2)
    Ellipse = mpatches.Ellipse((0.5, 0.5), 0.7, 0.2)
    Rombus = Patch(Path(
        *list(zip(*[
                (Path.MOVETO, [0.5, 0.6]),
                (Path.LINETO, [0.15, 0.5]),
                (Path.LINETO, [0.5, 0.4]),
                (Path.LINETO, [0.85, 0.5]),
                (Path.LINETO, [0.5, 0.6]),
            ]))[::-1]
            ))
    Arrow = Patch(Path(
        *list(zip(*[  # Can make any shape, just set coords in unit axes
                (Path.MOVETO, [0.15, 0.55]),
                (Path.LINETO, [0.15, 0.45]),
                (Path.LINETO, [0.65, 0.45]),
                (Path.LINETO, [0.6, 0.35]),
                (Path.LINETO, [0.85, 0.5]),
                (Path.LINETO, [0.6, 0.65]),
                (Path.LINETO, [0.65, 0.55]),
                (Path.LINETO, [0.15, 0.55]),
            ]))[::-1]
            ))

    def __init__(self, colour, shape, fill, number, cd=None, sd=None):
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
        if cd is None:
            self.cd = {0: "black", 1: "green", 2: "blue", 3: "red"}
        else:
            self.cd = cd
        if sd is None:
            self.sd = {0: "rectangle", 1: "ellipse", 2: "rombus", 3: "arrow"}
        else:
            self.sd = sd
        self.fd = {1: "none", 2: "hatched", 3: "filled"}
        self.nd = {1: "one", 2: "two", 3: "three"}

    def __str__(self):
        c = self.cd[self.c]
        s = self.sd[self.s]
        f = self.fd[self.f]
        n = self.nd[self.n]
        return f"colour: {c}, shape: {s}, fill: {f}, number: {n}"

    def __repr__(self):
        return f"<Set.card.Card object {self.id}>"

    def is_same(self, other):
        assert isinstance(other, Card)
        return self.id == other.id

    def form_set(self, this, that):
        """
        Value for each category is labeled 1,2,3
        Sum of values of one category of three cards
        is divisible by 3 only if all are equal or unequal
        if all category sums are divisible by three
        the mod of all separately is 0.

        _id is array with each category, and the mod operates elementwise
        sum is 0 only if self, this and that form set
        """
        ids = self._id + this._id + that._id
        return not sum(ids % 3)

    def make_blobs(self, ax):
        """
        Fills card with blobs only when needed
        Takes axes-object as arg to transform correctly within Axes
        """

        patches = []
        # Make correct shape
        if self.s == 0:  # Rectangle
            patch = copy(Card.Rectangle)
        elif self.s == 1:  # Ellipse
            patch = copy(Card.Ellipse)
        elif self.s == 2:  # Rombus
            patch = copy(Card.Rombus)
        elif self.s == 3:  # Arrow
            patch = copy(Card.Arrow)

        patch.set_linewidth(5)
        patch.set_color(self.cd[self.c])  # Make correct colour

        # Make correct fill
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

        # Make currect number, and place each nicely
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
        """ Returns shuffled full deck (all possible 81 cards) """
        deck = []
        for c in range(1, 4):
            for s in range(1, 4):
                for f in range(1, 4):
                    for n in range(1, 4):
                        deck.append(Card(c, s, f, n))
        np.random.shuffle(deck)
        return deck

    @staticmethod
    def id_list(deck):
        """ Convert list of Card to list of ids, for compression """
        return [card.id for card in deck]


def standard_card():
    # Plot single card for testing
    fig, ax = plt.subplots()
    try:
        C = Card(*[int(i) for i in sys.argv[1]])
    except:
        C = Card(1, 1, 1, 1)
    C.make_blobs(ax)
    ax.add_artist(C)
    plt.show()


if __name__ == "__main__":
    standard_card()