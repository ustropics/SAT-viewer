from imports import *
from utils import *

from static.css.styles import *

from components.sidebar import create_sidebar
from components.info_comp import create_composite_info
from components.info_proj import create_projection_info
from components.img_player import create_img_player

from data_prc import create_main_dict
from data_get import get_data_files_goes, get_data_files_hima
from data_plt import create_product


# Initialize the panel extension
pn.extension('terminal', **app_settings)


# Load in the data files
loc_data = get_json_data(location_data)
prd_data = get_json_data(product_data)
prj_data = get_json_data(projection_data)
sat_data = get_json_data(satellite_data)


# Initialize the main sidebar and main placeholder
sidebar = create_sidebar(loc_data, prd_data, prj_data, sat_data)
composite_page = create_composite_info('CIMSS True Color Corrected', loc_data, prd_data, sat_data, sidebar)
main_placeholder = pn.pane.Placeholder(composite_page)


# Identify the termainal and dropdown widgets
terminal = sidebar[0][1]
com_dropdown = sidebar[1][0][2]
loc_dropdown = sidebar[1][0][3]
sat_dropdown = sidebar[1][1][0]
prj_dropdown = sidebar[1][1][2]
json_update = sidebar[1][3][3]


# Export the main dictionary to a JSON file
def export_btn_fnc(event):
    create_main_dict(sidebar, loc_data, prd_data, prj_data, sat_data)
    export_json_file(terminal)


# Main function to update the main frame
def update_main_frame(event):
    if event.obj is com_dropdown:
        composite_page = create_composite_info(event.new, loc_data, prd_data, sat_data, sidebar)
        main_placeholder.update(composite_page)
        log_to_terminal(terminal, f"{event.new} composite selected...")
    if event.obj is prj_dropdown:
        projection_page = create_projection_info(event.new, prj_data)
        main_placeholder.update(projection_page)
        log_to_terminal(terminal, f"{event.new} projection selected...")
    if event.obj is loc_dropdown:
        log_to_terminal(terminal, f"{event.new} location selected...")
        pass
    if event.obj is sat_dropdown:
        log_to_terminal(terminal, f"{event.new} satellite selected...")
        composites = get_composites(sat_data, event.new)
        com_dropdown.options = composites
        com_dropdown.value = composites[0]
        pass


# Attach the watch function to the dropdowns to track changes
com_dropdown.param.watch(update_main_frame, 'value')
prj_dropdown.param.watch(update_main_frame, 'value')
loc_dropdown.param.watch(update_main_frame, 'value')
sat_dropdown.param.watch(update_main_frame, 'value')
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

def convert_datetime(obj):
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj


# Attach functions to the buttons
sidebar[0][0][0].on_click(run_app)
sidebar[0][0][1].on_click(lambda event: clear_terminal(terminal))
sidebar[1][3][4].on_click(lambda event: import_json_file(sidebar, loc_data, prd_data, prj_data, sat_data))
sidebar[1][3][5].on_click(export_btn_fnc)
sidebar[1][3][0].on_click(lambda event: create_movie_file(terminal))
sidebar[1][3][1].on_click(lambda event: create_animation_file(terminal))


# Create the app and serve it
pn.template.MaterialTemplate(
    site="",
    title="SAT-Viewer",
    sidebar=sidebar,
    main=main_placeholder
).servable();
