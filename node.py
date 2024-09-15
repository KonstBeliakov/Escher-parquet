import pygame


class Node:
    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self.activation_radius = 7
        self.radius = 5
        self.draw_node = True
        self.connections = []
        self.color = (0, 0, 0)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    def add_connection(self, new_node):
        self.connections.append(new_node)

    def draw(self, screen):
        if self.draw_node:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)

