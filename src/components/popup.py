import pygame as pg
from components.filehandler import get_resource_path
import os


''' This class is a popup component that can be in pygame projects.
    This class was used for the project to display temporary popups
    with a message.'''
class Popup:
    def __init__(self, text, duration=2000, font_size = 20, font_path=get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf"))):
        self.text = text
        self.font = pg.font.Font(font_path, font_size)
        self.duration = duration
        self.start_time = None
        self.active = False

    def show(self):
        self.start_time = pg.time.get_ticks()
        self.active = True

    def draw(self, screen):
        if not self.active:
            return
        
        elapsed_time = pg.time.get_ticks() - self.start_time
        if elapsed_time > self.duration:
            self.active = False
            return


        popup_surface = pg.Surface((300, 70), pg.SRCALPHA)
        popup_surface.fill((0, 0, 0, 180))  # Semi-transparent background

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(popup_surface.get_width() // 2, popup_surface.get_height() // 2))

        popup_surface.blit(text_surf, text_rect)
        popup_rect = popup_surface.get_rect(center=(screen.get_width() // 2, 50))

        screen.blit(popup_surface, popup_rect)
