

''' This class is responsible for managing the themes of the application.
    It has a dictionary of themes with their respective colors. It also
    has a method to toggle between the themes and a method to get the
    color of a specific key. '''
class ThemeManager:
    def __init__(self):
        self.themes = {
            "light": {"bg": (21, 178, 199), "text": (255, 255, 255), "button": (0, 0, 0)},
            "dark": {"bg": (50, 54, 63), "text": (255, 255, 255), "button": (255, 255, 255)}
        }
        self.current_theme = "light"

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"

    def get_color(self, key):
        return self.themes[self.current_theme][key]
