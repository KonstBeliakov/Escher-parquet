import pygame


class Node:
    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self.activation_radius = 7
        self.radius = 5
        self.draw_node = True
        self.connections = []
        self.color = (0, 0, 0)

        self.active = False

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    @property
    def connections_num(self):
        return len(self.connections)

    def add_connection(self, new_node):
        self.connections.append(new_node)

    def update(self, main_window):
        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2 <= self.activation_radius ** 2:
                    self.active = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.active = False
        if self.active:
            self.pos = pygame.mouse.get_pos()

    def draw(self, screen):
        if self.draw_node:
            pygame.draw.circle(screen, self.color, self.pos, self.radius, width=2 * self.active)

        for node in self.connections:
            pygame.draw.line(screen, self.color, self.pos, node.pos, 1)
