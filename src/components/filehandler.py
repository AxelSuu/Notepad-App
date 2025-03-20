import sys
import os


''' This function is used to get the absolute path to a resource, works for dev and for PyInstaller.
    This function is Operating System independent. Used for getting the path to the files.'''
def get_resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def get_data_dir():
    """Get the directory for saving user data"""
    # For Windows
    if os.name == 'nt':
        app_data = os.path.join(os.environ['APPDATA'], 'PygameNotepad')
    # For macOS
    elif sys.platform == 'darwin':
        app_data = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'PygameNotepad')
    # For Linux
    else:
        app_data = os.path.join(os.path.expanduser('~'), '.pygamenotepad')
    
    # Create directory if it doesn't exist
    os.makedirs(app_data, exist_ok=True)
    return app_data
