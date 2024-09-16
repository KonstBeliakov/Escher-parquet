from time import perf_counter

import numpy as np
import pygame
from random import randint

from node import Node
from figure import Figure, FigureTypes
import utils
from utils import *
from slider import Slider


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

        self.slider = Slider(pos=(10, 50), size=(100, 20), function=lambda: self.slider_update(),
                             max_value=10)

        self.map_moving = False
        self.last_click = None

    def slider_update(self):
        utils.node_radius = self.slider.value

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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.last_click = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    self.map_moving = False
                    self.last_click = None

            self.map_moving = not self.figure.dragging and not self.slider.dragging
            if self.map_moving and self.last_click is not None:
                utils.diplacement_vector += np.array(pygame.mouse.get_pos()) - np.array(self.last_click)
                self.last_click = pygame.mouse.get_pos()

            self.screen.fill((255, 255, 255))
            utils.transparent_surface = pygame.Surface((windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)),
                                                 pygame.SRCALPHA)

            self.figure.update(self)
            self.figure.draw(self.screen)

            text_surface = self.font.render("Node radius", True, (0, 0, 0))
            #text_rect = text_surface.get_rect(center=())
            self.screen.blit(text_surface, (10, 10))

            self.slider.update(self)
            self.slider.draw(self.screen)

            for text, time in self.hints:
                text_surface = self.font.render(text, True, (255, 0, 0))
                text_surface.set_alpha(int(max(0.0, (1 - (perf_counter() - time))) * 255))
                text_rect = text_surface.get_rect(center=(WIDTH // 2,
                                                          HEIGHT - 120 - (perf_counter() - time) * 25))
                self.screen.blit(text_surface, text_rect)
            self.screen.blit(utils.transparent_surface, (0, 0))
            pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()

    def add_hint(self, text):
        self.hints.append([text, perf_counter()])
