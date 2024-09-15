import pygame


class Node:
    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self.activation_radius = 7
        self.radius = 5
        self.draw_node = True
        self.color = (0, 0, 0)

        self.active = False

        self.__dict__['next'] = None
        self.__dict__['previous'] = None

    @property
    def pos(self):
        return self.x, self.y

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

    def add_next(self, new_node):
        self.next = new_node
        new_node.previous = self

    def add_previous(self, new_node):
        new_node.add_next(self)

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

    def update(self, main_window):
        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2 <= self.activation_radius ** 2:
                    self.active = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.active = False
        if self.active:
            self.pos = pygame.mouse.get_pos()

    def draw(self, screen):
        if self.draw_node:
            pygame.draw.circle(screen, self.color, self.pos, self.radius, width=2 * self.active)

        if self.next is not None:
            pygame.draw.line(screen, self.color, self.pos, self.next.pos, 1)
