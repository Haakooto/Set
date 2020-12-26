from matplotlib.axes import Axes
from copy import copy
from matplotlib.text import Text
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

T = Text((0, 0), "testtest")
# ax = TestAx(ax)
# print(type(ax))
# # ax.text(0.5,0.5,"testtest")
ax.text(T)
plt.show()
