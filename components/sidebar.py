from imports import *
from config import *
from utils import *

from static.css.styles import *

def create_sidebar(loc_data, prd_data, prj_data, sat_data):


    # Create the composite and location lists
    composites = [entry['name'] for entry in prd_data]
    locations = [entry['location'] for entry in loc_data]
    projections = [entry['name'] for entry in prj_data]
    satellites = [entry['id'] for entry in sat_data]  

    # Run and clear button widgets for sidebar
    run_btn = pn.widgets.Button(name='Run', button_type='primary')
    clear_btn = pn.widgets.Button(name='Clear', button_type='success')

    # Utility buttons
    export_video_btn = pn.widgets.Button(name='Create Video', button_type='primary', button_style='outline', width=340)
    export_anim_btn = pn.widgets.Button(name='Create Animation', button_type='primary', button_style='outline', width=340)
    export_json_btn = pn.widgets.Button(name='Create JSON', button_type='success', button_style='outline', width=340)
    import_json_btn = pn.widgets.Button(name='Import JSON', button_type='primary', button_style='outline', width=340)
    import_json_file = pn.widgets.FileInput(name='Import JSON', accept='.json', width=340)

    download_json_btn = pn.pane.Placeholder('')
    

    # Terminal output widget
    terminal = pn.widgets.Terminal(
        f'{console_msg.program_init_msg}\n{console_msg.program_welcome_msg}',
        name='Terminal',
        height=150,
        options=terminal_options
    )
        
    # Start datetime picker widget
    start_dt = pn.widgets.DatetimePicker(
        name='Start Date',
        value=init_os,
        enable_seconds=False, width=340)
    
    # End datetime picker widget
    end_dt = pn.widgets.DatetimePicker(
        name='End Date',
        value=init_dt,
        enable_seconds=False,
        width=340
    )
    
    # Composite dropdown widget
    composite_dropdown = pn.widgets.Select(
        name='Satellite Composites',
        value='CIMSS True Color Corrected',
        size=7,
        width=340,
        options=composites
    )

    # Location dropdown widget
    location_dropdown = pn.widgets.Select(
        name='Locations',
        size=1,
        width=340,
        options=locations
    )

    # Projection dropdown widget
    projection_dropdown = pn.widgets.Select(
        name='Projection',
        size=4,
        options=['Autoselect']+projections,
        value='Autoselect',
        width=340
    )

    # Satellite dropdown widget
    satellite_dropdown = pn.widgets.Select(
        name='Satellite Type',
        options=['Autoselect']+satellites,
        value='Autoselect',
        width=340
    )

    # Domain dropdown widget
    domain_dropdown = pn.widgets.Select(
        name='Domain',
        options=['Autoselect','CONUS', 'Full Disk'],
        value='Autoselect',
        width=340
    )

    # Create color picker and border width widgets
    border_color = pn.widgets.ColorPicker(name='Border Color', value='orange', width=160)
    border_width = pn.widgets.FloatInput(name='Border Width', value=0.5, width=160)

    # Create the location inputs projection setting text input widgets
    lat1_input = pn.widgets.TextInput(name='Northern Latitude', value='0', width=160)
    lat2_input = pn.widgets.TextInput(name='Southern Latitude', value='0', width=160)
    lon1_input = pn.widgets.TextInput(name='Western Longitude', value='0', width=160)
    lon2_input = pn.widgets.TextInput(name='Eastern Longitude', value='0', width=160)

    # Add location inputs to rows
    lat_container = pn.Row(lat1_input, lat2_input)
    lon_container = pn.Row(lon1_input, lon2_input)

    # Create the checkbox switch widgets for labels and borders
    lat_lon_label_switch = pn.widgets.Switch(name='Lat/Lon Labels', value=False, width=theme_settings['switch_width'])
    lat_lon_grid_switch = pn.widgets.Switch(name='Lat/Lon Grid', value=False, width=theme_settings['switch_width'])
    state_border_switch = pn.widgets.Switch(name='State Borders', value=True, width=theme_settings['switch_width'])
    country_border_switch = pn.widgets.Switch(name='Country Borders', value=True, width=theme_settings['switch_width'])
    water_border_switch = pn.widgets.Switch(name='Lake/River Borders', value=False, width=theme_settings['switch_width'])
    county_border_switch = pn.widgets.Switch(name='County Borders', value=False, width=theme_settings['switch_width'])

    # Text Labels for the switches
    daynight_switch_label = pn.widgets.StaticText(value='Include Day/Night Composite')
    lat_lon_grid_label = pn.widgets.StaticText(value='Lat/Lon Grid')
    lat_lon_label_label = pn.widgets.StaticText(value='Lat/Lon Labels')
    state_border_label = pn.widgets.StaticText(value='State Borders')
    country_border_label = pn.widgets.StaticText(value='Country Borders')
    water_border_label = pn.widgets.StaticText(value='Lake/River Borders')
    county_border_label = pn.widgets.StaticText(value='County Borders')
    border_color_label = pn.widgets.StaticText(value='Border Color')
    json_label = pn.widgets.StaticText(value='Import and Export JSON Files')

    # Create the main button row and terminal column for the sidebar
    main_btn_row = pn.Row(run_btn, clear_btn, width=300)
    terminal_col = pn.Column(main_btn_row, terminal)

    # Create the main switch rows
    switch_col1 = pn.Column(state_border_label, water_border_label, lat_lon_label_label)
    switch_col2 = pn.Column(state_border_switch, water_border_switch, lat_lon_label_switch)
    switch_col3 = pn.Column(country_border_label, county_border_label, lat_lon_grid_label)
    switch_col4 = pn.Column(country_border_switch, county_border_switch, lat_lon_grid_switch)

    # Create the specfic container rows
    switch_container = pn.Row(switch_col1, switch_col2, switch_col3, switch_col4)
    border_container = pn.Row(border_color, border_width)

    # Create the main and projection columns
    main_col = pn.Column(start_dt, end_dt, composite_dropdown, location_dropdown)
    proj_col = pn.Column(satellite_dropdown, domain_dropdown, projection_dropdown, lat_container, lon_container, switch_container, border_container)
    expo_col = pn.Column(export_video_btn, export_anim_btn, json_label, import_json_file, import_json_btn, export_json_btn, download_json_btn)

    # Create the tab container
    tab_container = pn.Tabs(('Main',main_col), ('Customize',proj_col), ('Utilities',''), ('Import/Export',expo_col), dynamic=True)

    # Create the sidebar
    sidebar = pn.Column(terminal_col, tab_container)

    return sidebar