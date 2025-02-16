from imports import *
from utils import *

from static.css.styles import *

from components.sidebar import create_sidebar
from components.info_comp import create_composite_info
from components.info_proj import create_projection_info
from components.img_player import create_img_player
from components.info_intro import create_intro_info
from components.modal import download_modal, modal_window, export_btn_fnc

from data_prc import create_main_dict
from data_get import get_data_files_goes, get_data_files_hima
from data_plt import create_product

# Initialize the panel extension
pn.extension('terminal', 'modal', **app_settings)


# Load in the data files
loc_data = get_json_data(location_data)
prd_data = get_json_data(product_data)
prj_data = get_json_data(projection_data)
sat_data = get_json_data(satellite_data)


# Initialize the main sidebar and main placeholder
sidebar = create_sidebar(loc_data, prd_data, prj_data, sat_data)
composite_page = create_intro_info(sidebar, prd_data)
main_placeholder = pn.pane.Placeholder(composite_page)


# Identify the terminal and dropdown widgets
terminal = sidebar[0][1]
com_dropdown = sidebar[1][0][2]
loc_dropdown = sidebar[1][0][3]
sat_dropdown = sidebar[1][1][0]
prj_dropdown = sidebar[1][1][2]
json_update = sidebar[1][3][3]


# Attach the watch function to the dropdowns to track changes
com_dropdown.param.watch(lambda event: update_main_frame(event, main_placeholder, sidebar, loc_data, prd_data, prj_data, sat_data), 'value')
prj_dropdown.param.watch(lambda event: update_main_frame(event, main_placeholder, sidebar, loc_data, prd_data, prj_data, sat_data), 'value')
loc_dropdown.param.watch(lambda event: update_main_frame(event, main_placeholder, sidebar, loc_data, prd_data, prj_data, sat_data), 'value')
sat_dropdown.param.watch(lambda event: update_main_frame(event, main_placeholder, sidebar, loc_data, prd_data, prj_data, sat_data), 'value')
json_update.param.watch(lambda event: import_json_file(sidebar, loc_data, prd_data, prj_data, sat_data), 'value')


# Run main app functions
def run_app(event):
    img_arr.clear()
    create_dirs(terminal)
    create_main_dict(sidebar, loc_data, prd_data, prj_data, sat_data)
    backup_json_file(terminal)

    if main_dict['bucket'] == 'noaa-himawari9':
        band_files = get_data_files_hima(terminal, sat_data)
    else:
        band_files = get_data_files_goes(terminal, sat_data)
    
    create_product(sidebar, terminal, band_files)
    img_player = create_img_player()
    main_placeholder.update(img_player)


# Attach functions to the buttons
sidebar[0][0][0].on_click(run_app)
sidebar[0][0][1].on_click(lambda event: clear_terminal(terminal))
sidebar[1][3][4].on_click(lambda event: import_json_file(sidebar, loc_data, prd_data, prj_data, sat_data))
sidebar[1][3][5].on_click(lambda event: export_btn_fnc(event, sidebar, loc_data, prd_data, prj_data, sat_data, terminal))
sidebar[1][3][0].on_click(lambda event: create_movie_file(terminal))
sidebar[1][3][1].on_click(lambda event: create_animation_file(terminal))


# Create the app and serve it
pn.template.MaterialTemplate(
    site="",
    title="SAT-Viewer",
    sidebar=sidebar,
    main=pn.Column(main_placeholder, modal_window)
).servable();