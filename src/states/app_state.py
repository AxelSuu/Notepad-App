import pygame as pg
from components.button import Button
from components.text import Text
from components.popup import Popup
from components.thememanager import ThemeManager
from states.base_state import BaseState


''' This class is a window responsible for managing which applications to run.
    It has buttons to navigate to other windows,
    and the possibility to change the theme of the application. '''
class AppState(BaseState):
    def __init__(self, statemanager):
        super().__init__()
        self.statemanager = statemanager
        self.button1_clicked = False
        self.button2_clicked = False
        self.button3_clicked = False
        self.button4_clicked = False
        self.background_color = (21, 178, 199)  # Blue background
        self.text = Text("App", (self.statemanager.screen_width // 2, self.statemanager.screen_height * 1 / 4 + 50), 36)
        self.button1 = Button(20, 20, 100, 30, 18, self.button1up_function, self.button1d_function)
        self.button2 = Button(20, 60, 150, 30, 18, self.button2up_function, self.button2d_function)
        self.button3 = Button(self.statemanager.screen_width / 2 - 150, self.statemanager.screen_height * 1 / 4 + 100, 100, 30, 18, self.button3up_function, self.button3d_function)
        self.button4 = Button(self.statemanager.screen_width / 2 + 50, self.statemanager.screen_height * 1 / 4 + 100, 100, 30, 18, self.button4up_function, self.button4d_function)
        self.fade_in(self.statemanager.screen, self.statemanager.theme.get_color("bg"))
        self.popup = Popup("Theme Changed")
        self.button_color = self.statemanager.theme.get_color("button")
        self.text_color = self.statemanager.theme.get_color("text")

    def enter(self):
        print("Entering Game State")

    def exit(self):
        self.statemanager.change_state("exit")

    def button1up_function(self):
        self.button1_clicked = True
    def button2up_function(self):
        self.button2_clicked = True
    def button1d_function(self):
        self.button1_clicked = False
        self.statemanager.change_state("menustate")
    def button2d_function(self):
        self.button2_clicked = False
        self.statemanager.theme.toggle_theme()
        self.popup.show()
    def button3up_function(self):
        self.button3_clicked = True
    def button3d_function(self):
        self.button3_clicked = False
        self.statemanager.change_state("writestate")
    def button4up_function(self):
        self.button4_clicked = True
    def button4d_function(self):
        self.button4_clicked = False

    def button_logic(self):
        if self.button1_clicked:
            self.button1.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Menu", pg.Color(self.statemanager.theme.get_color("text")))
        else:
            self.button1.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Menu", pg.Color(self.statemanager.theme.get_color("text")), 2)
        if self.button2_clicked:
            self.button2.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Change theme", pg.Color(self.statemanager.theme.get_color("text")), )
        else:
            self.button2.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Change theme", pg.Color(self.statemanager.theme.get_color("text")), 2)
        if self.button3_clicked:
            self.button3.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Notepad", pg.Color(self.statemanager.theme.get_color("text")), )
        else:
            self.button3.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Notepad", pg.Color(self.statemanager.theme.get_color("text")), 2)
        if self.button4_clicked:
            self.button4.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "App2", pg.Color(self.statemanager.theme.get_color("text")), )
        else:
            self.button4.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "App2", pg.Color(self.statemanager.theme.get_color("text")),2)
        self.text.render(self.statemanager.screen)

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.statemanager.change_state("exit")
            # check if button is clicked
            self.button1.event(event)
            self.button2.event(event)
            self.button3.event(event)

    def render(self):
        self.statemanager.screen.fill(self.statemanager.theme.get_color("bg"))
        self.button_logic()
        self.popup.draw(self.statemanager.screen)
    
    def fade_in(self, screen, color=(0, 0, 0), speed=5):
        fade = pg.Surface(screen.get_size())
        fade.fill(color)
        for alpha in range(0, 255, speed):
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(10)