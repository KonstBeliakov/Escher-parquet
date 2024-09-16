import numpy as np
from ctypes  import *
import pygame


scale = 1.0
diplacement_vector = np.array([0.0, 0.0])
node_radius = 5
transparent_surface = pygame.Surface((windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)),
                                     pygame.SRCALPHA)

def dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def mid(pos1, pos2):
    return (pos1[0] + pos2[0]) // 2, (pos1[1] + pos2[1]) // 2
