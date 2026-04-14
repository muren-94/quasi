import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.colors as colors
import matplotlib.pyplot as plt



def colorline(x, y, z, contour_start_value=0, contour_end_value=100, linewidth=5, alpha=1.0, cmap='coolwarm_r', linestyle='-', axis=None):

    z = np.asarray(z) * 100

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, array=z, cmap=cmap,  linewidth=linewidth, alpha=alpha, linestyle=linestyle, norm=colors.BoundaryNorm(boundaries=np.linspace(contour_start_value,contour_end_value,11), ncolors=256))

    if axis is not None:
        axis.add_collection(lc)
    else:
        ax = plt.gca()
        ax.add_collection(lc)

    return lc
