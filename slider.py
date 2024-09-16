import pygame


class Slider:
    def __init__(self, pos=(50, 50), size=(200, 10), function=None, max_value=100):
        self.pos = pos
        self.size = size

        self.function = function

        self.dragging = False

        self.handle_rect = pygame.Rect(self.x, self.y, self.size_y, self.size_y)

        self.slider_value = 0

        self.slider_color = (100, 100, 100)
        self.slider_handle_color = (50, 50, 200)

        self.handle_x = pos[0]

        self.max_value = max_value
        self.last_slider_value = self.value

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    @property
    def size(self):
        return self.size_x, self.size_y

    @size.setter
    def size(self, size):
        self.size_x, self.size_y = size

    @property
    def value(self):
        return int((self.handle_x - self.x) / (self.size_x - self.size_y) * self.max_value)

    def update(self, main_window):
        for event in main_window.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect((self.handle_x, self.y, self.size_y, self.size_y)).collidepoint(event.pos):
                    self.dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

    def draw(self, screen):
        if self.dragging:
            mouse_x = pygame.mouse.get_pos()[0]

            self.last_slider_value = self.value

            self.handle_x = max(self.x,
                                min(mouse_x - self.handle_rect.width // 2,
                                    self.x + self.size_x - self.handle_rect.width))

            if self.value != self.last_slider_value:
                self.function()

        pygame.draw.rect(screen, self.slider_color, (self.x, self.y, self.size_x, self.size_y))
        pygame.draw.rect(screen, self.slider_handle_color, (self.handle_x, self.y, self.size_y, self.size_y))

        # Отображаем текущее значение бегунка
        #font = pygame.font.SysFont("Arial", 24)
        #value_text = font.render(f"Значение: {slider_value}", True, (0, 0, 0))
        #screen.blit(value_text, (350, 300))
