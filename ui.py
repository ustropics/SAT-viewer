from imports import *
from config import *

from static.css.styles import *

def create_sidebar():

    run_btn = pn.widgets.Button(name='Run', button_type='primary')
    clear_btn = pn.widgets.Button(name='Clear', button_type='success')

    terminal = pn.widgets.Terminal(
    "Program initializing...\n🌎  Welcome to SAT-viewer v1.1!\n",
    name="Terminal",
    options=terminal_options,
    height=200,
    width= 340
    )

    start_dt = pn.widgets.DatetimePicker(name='Start Date', value=init_os, enable_seconds=False, width=340)
    end_dt = pn.widgets.DatetimePicker(name='End Date', value=init_dt, enable_seconds=False, width=340)

    main_btn_row = pn.Row(run_btn, clear_btn, width=340)

    row = pn.Column(main_btn_row, terminal, start_dt, end_dt, height=400)

    return row

def create_test_btn():
    button = pn.widgets.Button(name='Test', button_type='primary')
    return button


