import pygame as pg
from components.button import Button
from states.base_state import BaseState
from components.text import Text


''' This class is a window responsible for managing the main menu of the application.
    It has buttons to navigate to other windows, and the possibility to exit the application. '''
class MenuState(BaseState):
    def __init__(self, statemanager):
        super().__init__()
        self.statemanager = statemanager
        self.buttons = []
        self.button1_clicked = False
        self.button2_clicked = False
        self.BLACK = (0, 0, 0)
        self.background_color = (21, 178, 199)  # Blue background
        self.text = Text("Welcome to the App", (self.statemanager.screen_width // 2, self.statemanager.screen_height * 1 / 4 + 50), 36)
        self.button1 = Button(self.statemanager.screen_width / 2 - 50, self.statemanager.screen_height * 2 / 4 - 15, 100, 30, 18, self.button1up_function, self.button1d_function)
        self.button2 = Button(self.statemanager.screen_width / 2 - 50, self.statemanager.screen_height * 3 / 4 - 15, 100, 30, 18, self.button2up_function, self.button2d_function)
        self.fade_in(self.statemanager.screen, self.background_color)
        

    def button1up_function(self):
        self.button1_clicked = True
    def button2up_function(self):
        self.button2_clicked = True
    def button1d_function(self):
        self.button1_clicked = False
        self.statemanager.change_state("appstate")
    def button2d_function(self):
        self.button2_clicked = False
        self.exit()

    def button_logic(self):
        if self.button1_clicked:
            self.button1.draw(self.statemanager.screen, pg.Color(0, 150, 255), "Start", pg.Color(255, 255, 255))
        else:
            self.button1.draw(self.statemanager.screen, pg.Color(0,0,0), "Start", pg.Color(255, 255, 255), 2)
        if self.button2_clicked:
            self.button2.draw(self.statemanager.screen, pg.Color(0, 150, 255), "Quit", pg.Color(255, 255, 255), )
        else:
            self.button2.draw(self.statemanager.screen, pg.Color(0,0,0), "Quit", pg.Color(255, 255, 255), 2)
        self.text.render(self.statemanager.screen)

    def enter(self):
        pass
    def exit(self):
        self.statemanager.change_state("exit")


    def update(self):
        # close window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.statemanager.change_state("exit")

            # check if button is clicked
            self.button1.event(event)
            self.button2.event(event)


    def render(self):
        # Render buttons, text, etc.
        self.statemanager.screen.fill(self.background_color)  # Lightblue background
        self.button_logic()

    def fade_in(self, screen, color=(0, 0, 0), speed=5):
        fade = pg.Surface(screen.get_size())
        fade.fill(color)
        for alpha in range(100, 255, speed):
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(10)
