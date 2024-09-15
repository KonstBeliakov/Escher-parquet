import numpy as np
import pygame
from random import randint

from node import Node
from figure import Figure, FigureTypes
from utils import *


class MainWindow:
    def __init__(self):
        pygame.init()

        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Простое Pygame приложение")

        self.running = True

        self.figure_size = 300

        self.figure = Figure(pos=(400, 400), figure_type=FigureTypes.HEXAGON, size=self.figure_size)
        self.events = []

        self.fullscreen = False

    def update(self):
        if self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.fill((255, 255, 255))

            self.figure.update(self)
            self.figure.draw(self.screen)

            pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()
