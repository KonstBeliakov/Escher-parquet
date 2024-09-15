import pygame
from random import randint

from node import Node
from figure import Figure, FigureTypes


class MainWindow:
    def __init__(self):
        pygame.init()

        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Простое Pygame приложение")

        self.running = True

        self.fiure = Figure(pos=(200, 200))

        self.events = []

    def update(self):
        if self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.fill((255, 255, 255))

            self.fiure.update(self)
            self.fiure.draw(self.screen)

            pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()
