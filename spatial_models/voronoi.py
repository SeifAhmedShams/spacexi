import numpy as np
from scipy.spatial import cKDTree

XS = np.arange(0.5, 105, 1.0)
YS = np.arange(0.5, 68, 1.0)
GX, GY = np.meshgrid(XS, YS)
GRID = np.c_[GX.ravel(), GY.ravel()]


def get_players(row):
    pts, team = [], []
    for side, t in [("home", 1), ("away", 0)]:
        for c in row.index:
            if c.startswith(side + "_") and c.endswith("_x"):
                x, y = row[c], row[c[:-1] + "y"]
                if x == x and y == y:
                    pts.append((x, y))
                    team.append(t)
    return np.array(pts), np.array(team)


def voronoi_control(row):
    """Return a (68, 105) boolean grid: True where home is the nearest team."""
    pts, team = get_players(row)
    _, idx = cKDTree(pts).query(GRID)
    return (team[idx] == 1).reshape(GX.shape)
