import pygame as pg
from components.button import Button
from components.text import Text
from components.popup import Popup
from components.thememanager import ThemeManager
from states.base_state import BaseState
import os
import sys
from datetime import datetime
from components.filehandler import get_resource_path, get_data_dir


''' This class is a window responsible for managing the writing of notes.
    It has buttons to navigate to other windows, save notes, browse notes,
    change the theme of the application and write notes. '''
class WriteState(BaseState):
    def __init__(self, statemanager):
        super().__init__()
        self.statemanager = statemanager
        self.button1_clicked = False
        self.button2_clicked = False
        self.button3_clicked = False
        self.background_color = (21, 178, 199)  # Blue background
        self.text = Text("Notepad", (self.statemanager.screen_width // 2, self.statemanager.screen_height * 1 / 8), 36)
        self.button1 = Button(10, 20, 100, 30, 18, self.button1up_function, self.button1d_function)
        self.button2 = Button(10, 60, 150, 30, 18, self.button2up_function, self.button2d_function)
        self.button3 = Button(10, 100, 60, 30, 18, self.button3up_function, self.button3d_function)
        
        # Save and Browse buttons
        self.save_button = Button(self.statemanager.screen_width / 2 - 100, self.statemanager.screen_height * 3 / 4 + 120, 80, 30, 18, self.save_button_up, self.save_button_down)
        self.browse_button = Button(self.statemanager.screen_width / 2 + 20, self.statemanager.screen_height * 3 / 4 + 120, 80, 30, 18, self.browse_button_up, self.browse_button_down)
        self.save_clicked = False
        self.browse_clicked = False
        
        # Textbox properties
        self.textbox_active = False
        self.textbox_text = ""
        self.textbox_font = pg.font.Font(get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf")), 24)
        self.textbox_rect = pg.Rect(self.statemanager.screen_width / 2 - 200, self.statemanager.screen_height * 1 / 2 - 200, 400, 400)
        self.textbox_color_inactive = (255, 255, 255)
        self.textbox_color_active = (230, 230, 230)
        self.textbox_color = self.textbox_color_inactive
        self.textbox_border_color = (50, 50, 50)
        
        # Filename input box
        self.filename_active = False
        self.filename_text = ""
        self.filename_rect = pg.Rect(self.statemanager.screen_width / 2 - 100, self.statemanager.screen_height * 3 / 4 + 80, 200, 30)
        self.filename_color_inactive = (255, 255, 255)
        self.filename_color_active = (230, 230, 230)
        self.filename_color = self.filename_color_inactive
        self.filename_border_color = (50, 50, 50)
        self.filename_font = pg.font.Font(get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf")), 18)
        
        # File browser
        self.show_browser = False
        self.file_list = []
        self.selected_file = None
        self.scroll_y = 0
        self.browser_rect = pg.Rect(self.statemanager.screen_width / 2 - 150, 100, 300, 400)
        
        # Confirmation dialog
        self.show_confirm_dialog = False
        self.confirm_text = "Save note?"
        self.yes_button = Button(self.browser_rect.x + 50, self.browser_rect.y + 350, 80, 30, 18, self.yes_clicked, None)
        self.no_button = Button(self.browser_rect.x + 170, self.browser_rect.y + 350, 80, 30, 18, self.no_clicked, None)
        
        self.fade_in(self.statemanager.screen, self.statemanager.theme.get_color("bg"))
        self.popup = Popup("Theme Changed")
        self.button_color = self.statemanager.theme.get_color("button")
        self.text_color = self.statemanager.theme.get_color("text")
        
        # Notes directory - use user's app data folder instead of relative path
        self.notes_dir = os.path.join(get_data_dir(), "notes")
        os.makedirs(self.notes_dir, exist_ok=True)
        self.refresh_file_list()

    def refresh_file_list(self):
        try:
            self.file_list = [f for f in os.listdir(self.notes_dir) if f.endswith('.txt')]
            self.file_list.sort(reverse=True)  # Most recent first
        except:
            self.file_list = []

    def save_button_up(self):
        self.save_clicked = True

    def save_button_down(self):
        self.save_clicked = False
        if self.textbox_text.strip():
            self.show_confirm_dialog = True

    def browse_button_up(self):
        self.browse_clicked = True

    def browse_button_down(self):
        self.browse_clicked = False
        self.show_browser = not self.show_browser
        if self.show_browser:
            self.refresh_file_list()

    def yes_clicked(self):
        self.save_note()
        self.show_confirm_dialog = False

    def no_clicked(self):
        self.show_confirm_dialog = False

    # Fix file path separators in save_note
    def save_note(self):
        # Create notes directory if it doesn't exist
        os.makedirs(self.notes_dir, exist_ok=True)
        
        # Generate filename
        if self.filename_text.strip():
            safe_filename = ''.join(c for c in self.filename_text if c.isalnum() or c in (' ', '_', '-'))
            filename = os.path.join(self.notes_dir, f"{safe_filename}.txt")  # Fixed
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.notes_dir, f"note_{timestamp}.txt")  # Fixed
        
        
        # Write the text to the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.textbox_text)
        
        # Show confirmation message
        self.popup = Popup(f"Note saved as {os.path.basename(filename)}")
        self.popup.show()
        
        # Refresh file list
        self.refresh_file_list()

    def enter(self):
        print("Entering Write State")

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
        self.statemanager.change_state("appstate")

    def button_logic(self):
        if self.button1_clicked:
            self.button1.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Menu", pg.Color(self.statemanager.theme.get_color("text")))
        else:
            self.button1.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Menu", pg.Color(self.statemanager.theme.get_color("text")), 2)
        if self.button2_clicked:
            self.button2.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Change theme", pg.Color(self.statemanager.theme.get_color("text")))
        else:
            self.button2.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Change theme", pg.Color(self.statemanager.theme.get_color("text")), 2)
        if self.button3_clicked:
            self.button3.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "App", pg.Color(self.statemanager.theme.get_color("text")))
        else:
            self.button3.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "App", pg.Color(self.statemanager.theme.get_color("text")), 2)
            
        # Draw save and browse buttons
        if self.save_clicked:
            self.save_button.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Save", pg.Color(self.statemanager.theme.get_color("text")))
        else:
            self.save_button.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Save", pg.Color(self.statemanager.theme.get_color("text")), 2)
            
        if self.browse_clicked:
            self.browse_button.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Files", pg.Color(self.statemanager.theme.get_color("text")))
        else:
            self.browse_button.draw(self.statemanager.screen, pg.Color(self.statemanager.theme.get_color("button")), "Files", pg.Color(self.statemanager.theme.get_color("text")), 2)
            
        self.text.render(self.statemanager.screen)

    def handle_textbox_events(self, event):
        # Handle main textbox events
        if event.type == pg.MOUSEBUTTONDOWN and not self.show_browser and not self.show_confirm_dialog:
            # If the user clicked on the textbox
            if self.textbox_rect.collidepoint(event.pos):
                self.textbox_active = True
                self.filename_active = False
            elif self.filename_rect.collidepoint(event.pos):
                self.textbox_active = False
                self.filename_active = True
            else:
                self.textbox_active = False
                self.filename_active = False
            
            # Change the color of the textboxes based on active state
            self.textbox_color = self.textbox_color_active if self.textbox_active else self.textbox_color_inactive
            self.filename_color = self.filename_color_active if self.filename_active else self.filename_color_inactive
        
        if event.type == pg.KEYDOWN:
            if self.textbox_active:
                if event.key == pg.K_RETURN:
                    # Add a newline to the textbox
                    self.textbox_text += '\n'
                elif event.key == pg.K_BACKSPACE:
                    self.textbox_text = self.textbox_text[:-1]
                else:
                    self.textbox_text += event.unicode
            elif self.filename_active:
                if event.key == pg.K_RETURN:
                    # Try to save with the current filename
                    self.show_confirm_dialog = True
                elif event.key == pg.K_BACKSPACE:
                    self.filename_text = self.filename_text[:-1]
                else:
                    # Limit filename to 19 characters
                    if len(self.filename_text) < 19:
                        self.filename_text += event.unicode

        # Scrolling in file browser
        if self.show_browser and event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_y = min(0, self.scroll_y + 20)
            elif event.button == 5:  # Scroll down
                max_scroll = -max(0, len(self.file_list) * 30 - 350)
                self.scroll_y = max(max_scroll, self.scroll_y - 20)
            
            # File selection
            if self.browser_rect.collidepoint(event.pos) and not (self.browser_rect.y + 350 <= event.pos[1] <= self.browser_rect.y + 380):
                relative_y = event.pos[1] - self.browser_rect.y - 40 - self.scroll_y
                file_index = relative_y // 30
                if 0 <= file_index < len(self.file_list):
                    self.selected_file = self.file_list[file_index]
                    # Double click to load file
                    if event.button == 1 and pg.time.get_ticks() - getattr(self, 'last_click_time', 0) < 500:
                        self.load_selected_file()
                    self.last_click_time = pg.time.get_ticks()

    # Update other methods that use asset paths
    def load_selected_file(self):
        if not self.selected_file:
            return
            
        try:
            with open(os.path.join(self.notes_dir, self.selected_file), 'r', encoding='utf-8') as file:
                self.textbox_text = file.read()
            
            # Set filename without extension
            self.filename_text = os.path.splitext(self.selected_file)[0]
            
            # Close browser after loading
            self.show_browser = False
            self.popup = Popup(f"Loaded: {self.selected_file}")
            self.popup.show()
        except Exception as e:
            self.popup = Popup(f"Error loading file: {str(e)}")
            self.popup.show()

    def draw_textbox(self):
        # Draw the main textbox
        pg.draw.rect(self.statemanager.screen, self.textbox_color, self.textbox_rect)
        pg.draw.rect(self.statemanager.screen, self.textbox_border_color, self.textbox_rect, 2)
        
        # Draw the filename textbox
        pg.draw.rect(self.statemanager.screen, self.filename_color, self.filename_rect)
        pg.draw.rect(self.statemanager.screen, self.filename_border_color, self.filename_rect, 2)
        
        # Draw filename label
        #filename_label = Text("Filename:", (self.filename_rect.x, self.filename_rect.y - 25), 18)
        #filename_label.render(self.statemanager.screen)
        filename_label = self.filename_font.render("Filename:", True, (255, 255, 255))
        self.statemanager.screen.blit(filename_label, (self.filename_rect.x, self.filename_rect.y - 25))
        
        # Render filename text
        if self.filename_text:
            filename_surface = self.filename_font.render(self.filename_text, True, (0, 0, 0))
            self.statemanager.screen.blit(filename_surface, (self.filename_rect.x + 5, self.filename_rect.y + 5))
        
        # Render the main text
        text_color = (0, 0, 0)  # Black text
        
        # Split text by newlines first
        lines = []
        for paragraph in self.textbox_text.split('\n'):
            if not paragraph:
                lines.append('')
                continue
                
            # Word wrap within each paragraph
            max_width = self.textbox_rect.width - 10
            words = paragraph.split(' ')
            current_line = ''
            
            for word in words:
                test_line = current_line + word + ' '
                test_surface = self.textbox_font.render(test_line, True, text_color)
                if test_surface.get_width() <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + ' '
            
            lines.append(current_line)
        
        # Render lines
        visible_lines = min(len(lines), 8)  # Limit to how many can fit in the box
        for i in range(visible_lines):
            line = lines[i]
            line_surface = self.textbox_font.render(line, True, text_color)
            self.statemanager.screen.blit(line_surface, 
                                        (self.textbox_rect.x + 5, 
                                        self.textbox_rect.y + 5 + i * self.textbox_font.get_height()))

    # Fix the font loading in draw_file_browser and draw_confirmation_dialog
    def draw_file_browser(self):
        if not self.show_browser:
            return
            
        # Draw browser background
        browser_surface = pg.Surface((self.browser_rect.width, self.browser_rect.height))
        browser_surface.fill((240, 240, 240))
        
        # Draw title
        title_font = pg.font.Font(get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf")), 20)  # Fixed
        title_surf = title_font.render("File Browser", True, (0, 0, 0))
        browser_surface.blit(title_surf, (10, 10))
        
        # Draw files list
        file_font = pg.font.Font(get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf")), 16)  # Fixed
        
        # Rest of the method remains unchanged
        
        for i, file in enumerate(self.file_list):
            y_pos = 40 + i * 30 + self.scroll_y
            if 40 <= y_pos < self.browser_rect.height - 40:
                # Highlight selected file
                if file == self.selected_file:
                    pg.draw.rect(browser_surface, (200, 220, 255), (5, y_pos, self.browser_rect.width - 10, 25))
                
                # Draw filename
                file_surf = file_font.render(file, True, (0, 0, 0))
                browser_surface.blit(file_surf, (10, y_pos + 5))
        
        # Draw border
        pg.draw.rect(browser_surface, (0, 0, 0), (0, 0, self.browser_rect.width, self.browser_rect.height), 2)
        
        # Draw close button
        close_font = pg.font.Font(get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf")), 18)
        close_surf = close_font.render("Close", True, (0, 0, 0))
        close_rect = pg.Rect((self.browser_rect.width - 80) // 2, self.browser_rect.height - 35, 80, 30)
        pg.draw.rect(browser_surface, (200, 200, 200), close_rect)
        pg.draw.rect(browser_surface, (0, 0, 0), close_rect, 2)
        browser_surface.blit(close_surf, (close_rect.x + (close_rect.width - close_surf.get_width()) // 2, 
                                          close_rect.y + (close_rect.height - close_surf.get_height()) // 2))
        
        # Handle closing the browser
        mouse_pos = pg.mouse.get_pos()
        rel_pos = (mouse_pos[0] - self.browser_rect.x, mouse_pos[1] - self.browser_rect.y)
        if pg.mouse.get_pressed()[0] and close_rect.collidepoint(rel_pos):
            self.show_browser = False
        
        # Draw the browser
        self.statemanager.screen.blit(browser_surface, self.browser_rect)

    # Fix the font loading in draw_confirmation_dialog
    def draw_confirmation_dialog(self):
        if not self.show_confirm_dialog:
            return
            
        # Draw dialog background
        dialog_rect = pg.Rect(self.statemanager.screen_width // 2 - 150, self.statemanager.screen_height // 2 - 75, 300, 150)
        dialog_surface = pg.Surface((dialog_rect.width, dialog_rect.height))
        dialog_surface.fill((240, 240, 240))
        
        # Draw title
        dialog_font = pg.font.Font(get_resource_path(os.path.join("assets", "fonts", "Outfit-Regular.ttf")), 20)  # Fixed
        title_surf = dialog_font.render("Confirmation", True, (0, 0, 0))
        dialog_surface.blit(title_surf, 
                          ((dialog_rect.width - title_surf.get_width()) // 2, 20))
        
        # Draw message
        msg_surf = dialog_font.render(self.confirm_text, True, (0, 0, 0))
        dialog_surface.blit(msg_surf, 
                          ((dialog_rect.width - msg_surf.get_width()) // 2, 50))
        
        # Draw filename if available
        if self.filename_text:
            filename_surf = dialog_font.render(f'"{self.filename_text}.txt"', True, (0, 0, 0))
            dialog_surface.blit(filename_surf, 
                              ((dialog_rect.width - filename_surf.get_width()) // 2, 75))
        
        # Draw Yes/No buttons
        yes_rect = pg.Rect(50, 100, 80, 30)
        no_rect = pg.Rect(170, 100, 80, 30)
        
        pg.draw.rect(dialog_surface, (200, 200, 200), yes_rect)
        pg.draw.rect(dialog_surface, (0, 0, 0), yes_rect, 2)
        yes_surf = dialog_font.render("Yes", True, (0, 0, 0))
        dialog_surface.blit(yes_surf, (yes_rect.x + (yes_rect.width - yes_surf.get_width()) // 2, 
                                     yes_rect.y + (yes_rect.height - yes_surf.get_height()) // 2))
        
        pg.draw.rect(dialog_surface, (200, 200, 200), no_rect)
        pg.draw.rect(dialog_surface, (0, 0, 0), no_rect, 2)
        no_surf = dialog_font.render("No", True, (0, 0, 0))
        dialog_surface.blit(no_surf, (no_rect.x + (no_rect.width - no_surf.get_width()) // 2, 
                                    no_rect.y + (no_rect.height - no_surf.get_height()) // 2))
        
        # Draw border
        pg.draw.rect(dialog_surface, (0, 0, 0), (0, 0, dialog_rect.width, dialog_rect.height), 2)
        
        # Handle button clicks
        mouse_pos = pg.mouse.get_pos()
        rel_pos = (mouse_pos[0] - dialog_rect.x, mouse_pos[1] - dialog_rect.y)
        if pg.mouse.get_pressed()[0]:
            if yes_rect.collidepoint(rel_pos):
                self.save_note()
                self.show_confirm_dialog = False
            elif no_rect.collidepoint(rel_pos):
                self.show_confirm_dialog = False
        
        # Draw the dialog
        self.statemanager.screen.blit(dialog_surface, dialog_rect)

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.statemanager.change_state("exit")
            
            # Handle textbox events
            self.handle_textbox_events(event)
            
            # Check if buttons are clicked
            self.button1.event(event)
            self.button2.event(event)
            self.button3.event(event)
            self.save_button.event(event)
            self.browse_button.event(event)

    def render(self):
        self.statemanager.screen.fill(self.statemanager.theme.get_color("bg"))
        self.button_logic()
        self.draw_textbox()
        self.draw_file_browser()
        self.draw_confirmation_dialog()
        self.popup.draw(self.statemanager.screen)
    
    def fade_in(self, screen, color=(0, 0, 0), speed=5):
        fade = pg.Surface(screen.get_size())
        fade.fill(color)
        for alpha in range(0, 255, speed):
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pg.display.update()
            pg.time.delay(10)