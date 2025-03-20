import pygame as pg
from states.menu_state import MenuState
from states.app_state import AppState
from states.write_state import WriteState
from components.thememanager import ThemeManager
from components.filehandler import get_resource_path
import os


''' This class is a state manager that manages the different states of the application.
    It has a method to change the state of the application and a method to add states
    to the manager.'''
class StateManager:
    def __init__(self):
        pg.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pg.display
        self.screen.set_icon(pg.image.load(get_resource_path(os.path.join("assets", "imgs", "icon.png"))))
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Application")
        self.clock = pg.time.Clock()
        self.states = {}
        self.running = True
        self.theme = ThemeManager()
        self.state = MenuState(self)

    def run(self):
        while self.running:
            self.state.update()
            self.state.render()
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

    def change_state(self, state):
        if state == "appstate":
            self.state = AppState(self)
        elif state == "menustate":
            self.state = MenuState(self)
        elif state == "writestate":
            self.state = WriteState(self)
        elif state == "exit":
            self.running = False

    def add_state(self, name, state):
        self.states[name] = state

if __name__ == "__main__":
    statemanager = StateManager()
    statemanager.run()