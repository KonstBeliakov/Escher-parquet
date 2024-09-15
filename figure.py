import enum
from math import sin, cos, radians
import pygame

from node import Node
from utils import *


class FigureTypes(enum.Enum):
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

    def regular_polygon(self, n):
        self.nodes = [Node((self.x + sin(radians(i * 360 // n)) * (self.size // 2),
                            self.y + cos(radians(i * 360 // n)) * (self.size // 2))) for i in range(n)]
        for i in range(n):
            self.nodes[i].add_connection(self.nodes[(i - 1) % n])
            self.nodes[i].add_connection(self.nodes[(i + 1) % n])

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    def update(self, main_window):
        for node in self.nodes:
            node.update(main_window)

        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    closest_node = min(self.nodes, key=lambda node: dist(node.pos, event.pos))
                    next_node = closest_node.connections[0]
                    new_node = Node(mid(closest_node.pos, next_node.pos))

                    closest_node.remove_from_connections(next_node)
                    closest_node.add_connection(new_node)
                    next_node.add_connection(new_node)

                    self.nodes.append(new_node)
                if event.button == 3:
                    mouse_x, mouse_y = event.pos
                    for i, node in enumerate(self.nodes):
                        if (mouse_x - node.x) ** 2 + (mouse_y - node.y) ** 2 <= node.activation_radius ** 2:
                            n1, n2 = self.nodes[i].connections[:2]
                            self.nodes[i].delete_connections()
                            del self.nodes[i]
                            n1.add_connection(n2)

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)
