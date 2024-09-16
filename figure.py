import enum
from math import sin, cos, radians
from typing import Tuple

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
    def __init__(self,main_window, figure_type=FigureTypes.SQUARE, pos=(0, 0), size=100):
        self.main_window = main_window
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

        self.dragging = False

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

    def clone_related_nodes(self, node_pos, clone_pos):
        for node_number, node in enumerate(self.nodes):
            if dist(node_pos + self.pos, node.pos + clone_pos) < 10:
                return node_number

    def clones_related_nodes(self, node_pos):
        return [self.clone_related_nodes(node_pos, clone_pos) for clone_pos in self.clones_pos]

    def related_segment(self, node, node2) -> tuple:
        '''Returns the index of the clone and the two indices of the nodes that form the linked segment'''
        node_related = self.clones_related_nodes(node.pos)
        node2_related = self.clones_related_nodes(node2.pos)
        for i in range(len(self.clones_pos)):
            if node_related[i] is not None and node2_related[i] is not None:
                return i, node_related[i], node2_related[i]
        return None, None, None

    def update(self, main_window):
        for node in self.nodes:
            node.update(main_window, self.pos)

        self.dragging = any([node.dragging for node in self.nodes])

        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:                     # add a new node
                    closest_node = min(self.nodes, key=lambda node: dist(node.screen_pos(self.pos), event.pos))
                    next_node = closest_node.next
                    clone_idx, related_node_idx, related_node2_idx = self.related_segment(closest_node, next_node)

                    new_node = Node(figure=self, pos=(closest_node.pos + next_node.pos) // 2)

                    new_clone_node = Node(figure=self,
                                          pos=(self.nodes[related_node_idx].pos + self.nodes[related_node2_idx].pos) // 2)
                    if self.nodes[related_node_idx].next == self.nodes[related_node2_idx]:
                        self.nodes[related_node_idx].next = new_clone_node
                        new_clone_node.next = self.nodes[related_node2_idx]
                    elif self.nodes[related_node2_idx].next == self.nodes[related_node_idx]:
                        self.nodes[related_node2_idx].next = new_clone_node
                        new_clone_node.next = self.nodes[related_node_idx]

                    self.nodes.append(new_clone_node)

                    closest_node.next = new_node
                    new_node.next = next_node

                    self.nodes.append(new_node)
                if event.button == 3:                         # delete a node
                    for i, node in enumerate(self.nodes):
                        if dist(node.screen_pos(self.pos), event.pos) <= node.activation_radius:
                            prev_node = self.nodes[i].previous
                            next_node = self.nodes[i].next

                            _, related_node_idx, related_node2_idx = self.related_segment(prev_node, next_node)
                            if related_node_idx is not None and related_node2_idx is not None:
                                self.nodes[i].delete_connections()
                                del self.nodes[i]
                                prev_node.next = next_node
                            else:
                                self.main_window.add_hint('Only degree 2 points can be deleted')

                            clone_idx, related_node_idx, related_node2_idx = self.related_segment(prev_node, next_node)

                            if related_node_idx is not None and related_node2_idx is not None:
                                n1, n2 = self.nodes[related_node_idx], self.nodes[related_node2_idx]

                                if n1.next.next == n2:
                                    self.del_node(n1.next)
                                    n1.next = n2
                                elif n2.next.next == n1:
                                    self.del_node(n2.next)
                                    n2.next = n1

    def del_node(self, node):
        for i in range(len(self.nodes)-1, -1, -1):
            if self.nodes[i] == node:
                self.nodes[i].delete_connections()
                del self.nodes[i]
                break

    def draw(self, screen):
        for clone_pos in self.clones_pos:
            for node in self.nodes:
                node.draw(screen, clone_pos, color=self.clone_color)

        for node in self.nodes:
            node.draw(screen, self.pos, color=self.color)
