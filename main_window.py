from time import perf_counter

import numpy as np
import pygame
from random import randint

from node import Node
from figure import Figure, FigureTypes
import utils
from utils import *


WIDTH, HEIGHT = 800, 600


class MainWindow:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Простое Pygame приложение")

        self.running = True

        self.figure_size = 300

        self.figure = Figure(self, pos=(400, 400), figure_type=FigureTypes.HEXAGON, size=self.figure_size)
        self.events = []

        self.fullscreen = False

        self.hints = []

        self.font_size = 20
        self.font = pygame.font.SysFont("Arial", self.font_size)

    def update(self):
        if self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        utils.scale *= 1.1
                    elif event.y < 0:
                        utils.scale /= 1.1

            self.screen.fill((255, 255, 255))

            self.figure.update(self)
            self.figure.draw(self.screen)

            for text, time in self.hints:
                text_surface = self.font.render(text, True, (255, 0, 0))
                text_surface.set_alpha(int(max(0.0, (1 - (perf_counter() - time))) * 255))
                text_rect = text_surface.get_rect(center=(WIDTH // 2,
                                                          HEIGHT - 120 - (perf_counter() - time) * 25))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()

    def add_hint(self, text):
        self.hints.append([text, perf_counter()])
