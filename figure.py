import enum
from math import sin, cos, radians
import pygame
import numpy as np

from node import Node
from utils import *


class FigureTypes(enum.Enum):
    NO_FIGURE = 0
    SQUARE = 1
    TRIANGLE = 2
    HEXAGON = 3


class Figure:
    def __init__(self, figure_type=FigureTypes.SQUARE, pos=(0, 0), size=100):
        self.size = size
        self.pos = pos
        self.nodes = []
        match figure_type:
            case FigureTypes.SQUARE:
                self.regular_polygon(4)
            case FigureTypes.TRIANGLE:
                self.regular_polygon(3)
            case FigureTypes.HEXAGON:
                self.regular_polygon(6)

        self.clone_color = (0, 0, 0, 100)
        self.color = (0, 200, 0, 255)

        self.clones_pos = []
        n = 6
        for i in range(n):
            a = self.nodes[i].pos + self.pos
            b = self.nodes[(i + 1) % n].pos + self.pos
            m = (a + b) // 2
            self.clones_pos.append(self.pos + 2 * (m - self.pos))

    def regular_polygon(self, n):
        self.nodes = [Node(self, (sin(radians((i - 0.5) * 360 // n)) * (self.size // 2),
                                  cos(radians((i - 0.5) * 360 // n)) * (self.size // 2))) for i in range(n)]
        for i in range(n):
            self.nodes[i].next = self.nodes[(i + 1) % n]

    @property
    def pos(self):
        return np.array([self.x, self.y])

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    def update(self, main_window):
        for node in self.nodes:
            node.update(main_window, self.pos)

        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    closest_node = min(self.nodes, key=lambda node: dist(node.pos, event.pos))
                    next_node = closest_node.next
                    new_node = Node(mid(closest_node.pos, next_node.pos))

                    closest_node.next = new_node
                    new_node.next = next_node

                    self.nodes.append(new_node)
                if event.button == 3:
                    mouse_x, mouse_y = event.pos
                    for i, node in enumerate(self.nodes):
                        if (mouse_x - node.x) ** 2 + (mouse_y - node.y) ** 2 <= node.activation_radius ** 2:
                            prev_node = self.nodes[i].previous
                            next_node = self.nodes[i].next
                            print(prev_node, next_node)
                            self.nodes[i].delete_connections()
                            del self.nodes[i]
                            prev_node.next = next_node

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen, self.pos, color=self.color)

        for clone_pos in self.clones_pos:
            for node in self.nodes:
                node.draw(screen, clone_pos, color=self.clone_color)
