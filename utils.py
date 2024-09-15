import numpy as np


scale = 1.0
diplacement_vector = np.array([0.0, 0.0])


def dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def mid(pos1, pos2):
    return (pos1[0] + pos2[0]) // 2, (pos1[1] + pos2[1]) // 2
