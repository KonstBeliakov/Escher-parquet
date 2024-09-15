import pygame
import numpy as np


class Node:
    def __init__(self, figure, pos=(0, 0)):
        self.figure = figure
        self.pos = pos
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
        self.x, self.y = pos

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
                mouse_x, mouse_y = event.pos
                x = self.x + figure_position[0]
                y = self.y + figure_position[1]
                if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= self.activation_radius ** 2:
                    self.active = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.active = False
        if self.active:
            self.pos = (pygame.mouse.get_pos()[0] - figure_position[0], pygame.mouse.get_pos()[1] - figure_position[1])

    def draw(self, screen, figure_position=(0, 0), color=(0, 0, 0)):
        surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)

        pos = (self.x + figure_position[0], self.y + figure_position[1])
        if self.draw_node:
            pygame.draw.circle(surface, color, pos, self.radius, width=2 * self.active)

        if self.next is not None:
            next_pos = (self.next.pos[0] + figure_position[0], self.next.pos[1] + figure_position[1])
            pygame.draw.line(surface, color, pos, next_pos, 1)

        screen.blit(surface, (0, 0))
