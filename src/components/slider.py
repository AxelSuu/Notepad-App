import pygame as pg


''' This class is a slider component that can be used in pygame projects.
    This class was never used for the project, but it can be used in the future.'''
class Slider:
    def __init__(self, x, y, min_value, max_value, start_value):
        self.rect = pg.Rect(x, y, 200, 10)
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.dragging = False

    def draw(self, screen):
        pg.draw.rect(screen, (200, 200, 200), self.rect)
        handle_x = self.rect.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width
        pg.draw.circle(screen, (0, 128, 255), (int(handle_x), self.rect.y + 5), 8)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            self.value = max(self.min_value, min(self.max_value, self.min_value + rel_x / self.rect.width * (self.max_value - self.min_value)))
