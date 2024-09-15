import pygame
from random import randint

from node import Node


class MainWindow:
    def __init__(self):
        pygame.init()

        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Простое Pygame приложение")

        self.running = True

        self.nodes = [Node((randint(100, 500), randint(100, 500))) for _ in range(10)]

        for i in range(10):
            for j in range(1, 3):
                self.nodes[i].add_connection(self.nodes[(i + j) % 10])

        self.events = []

    def update(self):
        if self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.fill((255, 255, 255))

            for node in self.nodes:
                node.update(self)
                node.draw(self.screen)

            pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()
