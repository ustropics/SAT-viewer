from imports import *
from utils import *

from static.css.styles import *
from ui import create_sidebar, create_test_btn
from data_prc import create_main_dict
from data_get import get_data_files

# Initialize the app components
pn.extension(
    'terminal',
    console_output='disable',
    design='material',
    global_css=[':root {--design-primary-color: #782F40}'],
    theme='dark',
    raw_css=[css]
    )

# Initialize the app components
sidebar = create_sidebar()
test_btn = create_test_btn()
terminal = sidebar[1]
terminal.style = {'font-size': '6px'}

# Run main app functions
def run_app(event):
    create_dirs()
    log_to_terminal(terminal, '📂  Directories created...')
    create_main_dict(sidebar)
    get_data_files(terminal)

# Attach the functions to the buttons
sidebar[0][0].on_click(run_app)
sidebar[0][1].on_click(lambda event: clear_terminal(terminal))

# Create the app and serve it
pn.template.MaterialTemplate(
    site="Panel",
    title="Getting Started App",
    sidebar=sidebar,
    main=test_btn
).servable();
