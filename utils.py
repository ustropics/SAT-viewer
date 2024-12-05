from imports import *
from config import *

def create_dirs():
    """Creates the necessary directories for data storage."""
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)

def clean_dt_values(dt_obj):
    """Cleans the datetime values for year, day, hour, and minute."""
    yr = dt_obj.year
    dy = dt_obj.timetuple().tm_yday
    hr = dt_obj.hour
    mn = dt_obj.minute
    return yr, dy, hr, mn

def test_print():
    """Test print the main_dict."""
    for item in main_dict:
        print(item, main_dict[item])

def log_to_terminal(terminal, message):
    """Logs a message to the given terminal."""
    if terminal:
        terminal.write(f"\n{message}")
    else:
        raise ValueError('Terminal instance is not provided.')

def clear_terminal(terminal):
    """Clears the terminal and logs a message."""
    if terminal:
        terminal.write('\nTerminal cleared...')
        terminal.clear()
    else:
        raise ValueError("Terminal instance is not provided.")

