import pygame as pg
from components.filehandler import get_resource_path
import os


''' This class is a text component that can be used in pygame projects.
    This class was used for the project to display text on the screen.
    It has three methods, one for rendering, one for typing text and
    one for glowing text when hovering over with the mouse.'''
class Text:
    def __init__(self, text, position, font_size=30, color=(255, 255, 255), font_path=get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf"))):
        self.text = text
        self.position = position
        self.font_size = font_size
        self.color = color
        self.font = pg.font.Font(font_path, font_size)

    def render(self, surface):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.position)
        surface.blit(self.text_surface, self.text_rect)

    def typing_text(screen, text, font, x, y, speed=50):
        displayed_text = ""
        for char in text:
            displayed_text += char
            screen.fill((0, 0, 0))
            text_surf = font.render(displayed_text, True, (255, 255, 255))
            screen.blit(text_surf, (x, y))
            pg.display.update()
            pg.time.delay(speed)

    def glowing_text(screen, text, font, x, y, color, glow_speed=5):
        glow = 50
        while True:
            glow = (glow + glow_speed) % 255
            text_surf = font.render(text, True, (glow, glow, glow))
            screen.fill((0, 0, 0))
            screen.blit(text_surf, (x, y))
            pg.display.update()
            pg.time.delay(50)
