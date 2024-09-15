import pygame
import numpy as np

import utils
from utils import *


class Node:
    def __init__(self, figure, pos=(0, 0)):
        self.figure = figure
        self.x, self.y = pos
        self.activation_radius = 7
        self.radius = 5
        self.draw_node = True

        self.active = False

        self.__dict__['next'] = None
        self.__dict__['previous'] = None

    @property
    def pos(self):
        return np.array([self.x, self.y])

    @pos.setter
    def pos(self, pos):
        dx, dy = pos - self.pos
        old_x, old_y = self.pos
        self.x, self.y = pos
        for clone_nodes_pos in self.figure.clone_nodes_pos:
            for node_number, node_pos in enumerate(clone_nodes_pos):
                if abs(old_x + self.figure.pos[0] - node_pos[0]) < 5 and abs(old_y + self.figure.pos[1] - node_pos[1]) < 5:
                    self.figure.nodes[node_number].__dict__['x'] += dx
                    self.figure.nodes[node_number].__dict__['y'] += dy

    def screen_pos(self, figure_pos):
        return ((utils.diplacement_vector[0] + self.x + figure_pos[0]) * utils.scale,
                (utils.diplacement_vector[1] + self.y + figure_pos[1]) * utils.scale)

    def __setattr__(self, key, value):
        if key == 'next':
            if getattr(self, 'next', None) is not None:
                self.next.__dict__['previous'] = None
            self.__dict__[key] = value
            if value is not None:
                value.__dict__['previous'] = self
        elif key == 'previous':
            if getattr(self, 'previous', None) is not None:
                self.previous.__dict__['next'] = None
            self.__dict__[key] = value
            if value is not None:
                value.__dict__['next'] = self
        else:
            super().__setattr__(key, value)

    def remove_from_connections(self, node):
        if self.previous == node:
            self.previous.next = None
            self.previous = None

        if self.next == node:
            self.next.previous = None
            self.next = None

    def delete_connections(self):
        if self.next is not None:
            self.next.previous = None
            self.next = None

        if self.previous is not None:
            self.previous.next = None
            self.previous = None

    def update(self, main_window, figure_position=(0, 0)):
        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if dist(event.pos, self.screen_pos(figure_position)) <= self.activation_radius:
                    self.active = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.active = False
        if self.active:
            self.pos = (self.x + (np.array(pygame.mouse.get_pos()[0]) - self.screen_pos(figure_position)[0]) * utils.scale,
                        self.y + (np.array(pygame.mouse.get_pos()[1]) - self.screen_pos(figure_position)[1]) * utils.scale)

    def draw(self, screen, figure_position=(0, 0), color=(0, 0, 0)):
        surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)

        if self.draw_node:
            pygame.draw.circle(surface, color, self.screen_pos(figure_position), self.radius, width=2 * self.active)

        if self.next is not None:
            pygame.draw.line(surface, color, self.screen_pos(figure_position),
                             self.next.screen_pos(figure_position), 1)

        screen.blit(surface, (0, 0))
