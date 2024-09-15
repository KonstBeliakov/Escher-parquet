import enum
from math import sin, cos, radians
import pygame
import numpy as np

from node import Node
from utils import *
import utils


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

        self.last_click = None
        self.map_moving = False

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

    @property
    def clone_nodes_pos(self):
        return [[node.pos + clone_pos for node in self.nodes] for clone_pos in self.clones_pos]

    def update(self, main_window):
        for node in self.nodes:
            node.update(main_window, self.pos)

        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, node in enumerate(self.nodes):
                        if dist(node.screen_pos(self.pos), event.pos) <= node.activation_radius:
                            self.map_moving = False
                            break
                    else:
                        self.map_moving = True
                        self.last_click = event.pos
                if event.button == 2:
                    closest_node = min(self.nodes, key=lambda node: dist(node.screen_pos(self.pos), event.pos))
                    next_node = closest_node.next
                    new_node = Node(figure=self, pos=(closest_node.pos + next_node.pos) // 2)

                    closest_node.next = new_node
                    new_node.next = next_node

                    self.nodes.append(new_node)
                if event.button == 3:
                    for i, node in enumerate(self.nodes):
                        if dist(node.screen_pos(self.pos), event.pos) <= node.activation_radius:
                            prev_node = self.nodes[i].previous
                            next_node = self.nodes[i].next
                            self.nodes[i].delete_connections()
                            del self.nodes[i]
                            prev_node.next = next_node
            if event.type == pygame.MOUSEBUTTONUP:
                self.map_moving = False

        if self.map_moving:
            utils.diplacement_vector += np.array(pygame.mouse.get_pos()) - np.array(self.last_click)
            self.last_click = pygame.mouse.get_pos()

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen, self.pos, color=self.color)

        for clone_pos in self.clones_pos:
            for node in self.nodes:
                node.draw(screen, clone_pos, color=self.clone_color)
