from collections import defaultdict
from functools import reduce
import math
import textwrap

import numpy as np

from matplotlib import artist
import matplotlib.axes as maxes
import matplotlib.cbook as cbook
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
import matplotlib.docstring as docstring
import matplotlib.scale as mscale
import matplotlib.transforms as mtransforms
from matplotlib.axes import Axes, rcParams
from matplotlib.axes._base import _axis_method_wrapper
from matplotlib.transforms import Bbox
from matplotlib.tri.triangulation import Triangulation

from matplotlib.offsetbox import DrawingArea

class DrawingArea(DrawingArea):
    def set_xycoords(self, xycoords):
        self.xycoords = xycoords

    def _get_position_xy(self, renderer):
        """Return the pixel position of the annotated point."""
        x, y = self.xy
        return self._get_xy(renderer, x, y, self.xycoords)

    def _get_ref_xy(self, renderer):
        return self._get_xy(renderer, *self.xy, self.xycoords)

    def _get_xy(self, renderer, x, y, s):
        return self._get_xy_transform(renderer, s).transform(x, y)

    def _get_xy_transform(self, renderer, s):
        if isinstance(s, Artist):
            bbox = s.get_window_extent(renderer)
            return BboxTransformTo(bbox)
