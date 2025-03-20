import pygame as pg
from components.filehandler import get_resource_path
import os


''' This class is a button component that can be used in pygame projects.
    This class was used for the project to create buttons with text on them.
    It includes the possibility for an action when the button is clicked.
    It has two methods, one for drawing the button and the hover effect,
    one for handling mouse click events.'''
class Button:
    def __init__(self, x, y, width, height, fontsize, action1=None, action2=None, hover_color=(0, 150, 255)):
        self.action1 = action1
        self.action2 = action2
        self.font = get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf"))
        self.rect = pg.Rect(x, y, width, height)
        self.fontsize = fontsize
        self.font = pg.font.Font(self.font, self.fontsize)
        self.hover_color = hover_color
        self.grow = False  # Track hover state
        self.clicked = False  # Track click state

    def draw(self, surface, color, text, text_color, border=0):
        mouse_pos = pg.mouse.get_pos()
        
        # Scale button size on hover
        if self.rect.collidepoint(mouse_pos):
            self.grow = True
        else:
            self.grow = False
        
        size_multiplier = 1.1 if self.grow else 1.0
        new_rect = self.rect.inflate(self.rect.width * (size_multiplier - 1), self.rect.height * (size_multiplier - 1))

        pg.draw.rect(surface, self.hover_color if self.grow else color, new_rect, border)
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        if self.grow:
            surface.blit(text_surface, (new_rect.x + 30, new_rect.y + 5))
        else:
            surface.blit(text_surface, text_rect)

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action1:
                self.clicked = True
                self.action1()
        if event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.action2:
                self.clicked = False
                self.action2()
