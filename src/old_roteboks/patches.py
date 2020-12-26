import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, RegularPolygon
import sys
import os
import time


fig, ax = plt.subplots()

R1 = Rectangle((0.3, 0.5), 0.2, 0.2, color="b", hatch="x+", fill=False)

ax.add_artist(R1)

plt.show()


