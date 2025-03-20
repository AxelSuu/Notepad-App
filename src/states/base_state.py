# Description: Base class for all states
import random
import pygame as pg


''' This is a parent class for shared methods and attributes
    for the windows in the application. '''
class BaseState:
    def __init__(self):
        pass

    def screenshake(screen, intensity=10, duration=500):
        """For screen shaking."""

        start_time = pg.time.get_ticks()
        while pg.time.get_ticks() - start_time < duration:
            x_offset = random.randint(-intensity, intensity)
            y_offset = random.randint(-intensity, intensity)
            screen.blit(screen, (x_offset, y_offset))
            pg.display.update()
            pg.time.delay(50)

    def exit(self):
        """Called when the state is exited."""
        pass

    def update(self):
        """Update the state. This method should be overridden by derived classes."""
        pass

    def render(self):
        """Render the state. This method should be overridden by derived classes."""
        pass

    def handle_events(self):
        """Handle events. This method should be overridden by derived classes."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()