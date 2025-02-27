import panel as pn
from imports import *
from utils import *

from static.css.styles import *
from components.sidebar import create_sidebar
from components.info_comp import create_composite_info
from components.info_proj import create_projection_info
from components.img_player import create_img_player
from components.info_intro import create_intro_info
from components.modal import (
    download_modal, modal_window, json_btn_fnc, movie_btn_fnc, animation_btn_fnc, process_msg_modal       
)

from data_prc import create_main_dict
from data_get import get_data_files_goes, get_data_files_hima, get_data_files_mtl1
from data_plt import create_product

# Define allowed WebSocket origins
public_ip = "satviewer.com"

def create_app():
    pn.extension(
        'terminal', 'modal',
        **app_settings
    )

    def get_initial_datetimes():
        init_dt = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        init_os = init_dt - timedelta(minutes=10)
        return init_os, init_dt

    def update_datetime():
        init_os, init_dt = get_initial_datetimes()
        sidebar[1][0][0].value = init_os
        sidebar[1][0][1].value = init_dt

    pn.state.onload(update_datetime)
    header_container = pn.pane.Placeholder()

    def update_player(img_tabs, urls):
        # Create the header player with proper steps
        player = pn.widgets.Player(
            start=0,
            end=len(urls) - 1,
            value=0,
            loop_policy='loop',
            show_loop_controls=False,
            interval=340,
            align='center',
            styles={"border-radius": "10px", "padding-top": "20px"}
        )
        
        # When player value changes, update the active tab.
        def update_tab(event):
            img_tabs.active = event.new
        player.param.watch(update_tab, 'value')
        
        # When the active tab changes (e.g., user clicks a tab), update the player value.
        def update_player_value(event):
            player.value = event.new
        img_tabs.param.watch(update_player_value, 'active')
        
        header_content = pn.Row(pn.layout.HSpacer(), player, pn.layout.HSpacer())
        header_container.update(header_content)

    loc_data = get_json_data(location_data)
    prd_data = get_json_data(product_data)
    prj_data = get_json_data(projection_data)
    sat_data = get_json_data(satellite_data)

    sidebar = create_sidebar(loc_data, prd_data, prj_data, sat_data)
    composite_page = create_intro_info(sidebar, prd_data)
    main_placeholder = pn.pane.Placeholder(composite_page)

    terminal = sidebar[0][1]
    com_dropdown = sidebar[1][0][2]
    loc_dropdown = sidebar[1][0][3]
    sat_dropdown = sidebar[1][1][0]
    prj_dropdown = sidebar[1][1][2]
    json_update = sidebar[1][3][3]

    intro_panel = create_intro_info(sidebar, prd_data)

    def update(event):
        update_main_frame(event, main_placeholder, sidebar, loc_data, prd_data, prj_data, sat_data)

    com_dropdown.param.watch(update, 'value')
    prj_dropdown.param.watch(update, 'value')
    loc_dropdown.param.watch(update, 'value')
    sat_dropdown.param.watch(update, 'value')
    json_update.param.watch(lambda event: import_json_file(sidebar, loc_data, prd_data, prj_data, sat_data), 'value')

    def run_app(event):
        img_arr.clear()
        dt_arr.clear()
        process_msg_modal()
        create_dirs(terminal)
        create_main_dict(sidebar, loc_data, prd_data, prj_data, sat_data)
        backup_json_file(terminal)

        if main_dict['bucket'] == 'noaa-himawari9':
            band_files = get_data_files_hima(terminal, sat_data)
        elif main_dict['bucket'] == 'mti1':
            band_files = get_data_files_mtl1(terminal, sat_data)
        else:
            band_files = get_data_files_goes(terminal, sat_data)

        create_product(sidebar, terminal, band_files)
        update_tooltip(1)
        img_tabs, urls = create_img_player()
        print("img_tabs", len(img_tabs))
        print("urls", len(urls))
        print("dt_arr", len(dt_arr))
        for item in dt_arr:
            print(item)
        main_placeholder.update(pn.Column(img_tabs))
        update_player(img_tabs, urls)

    sidebar[0][0][0].on_click(run_app)
    sidebar[0][0][1].on_click(lambda event: clear_terminal(terminal, main_placeholder, header_container, intro_panel))
    sidebar[1][3][4].on_click(lambda event: import_json_file(sidebar, loc_data, prd_data, prj_data, sat_data))
    sidebar[1][3][5].on_click(lambda event: json_btn_fnc(event, sidebar, loc_data, prd_data, prj_data, sat_data, terminal))
    sidebar[1][3][0].on_click(lambda event: movie_btn_fnc(event, terminal))
    sidebar[1][3][1].on_click(lambda event: animation_btn_fnc(event, terminal))

    def resize_terminal():
        terminal.sizing_mode = "fixed"
        terminal.width = 320

    pn.state.onload(resize_terminal)

    return pn.template.MaterialTemplate(
        site="",
        title="SAT-Viewer",
        header=header_container,
        sidebar=sidebar,
        main=pn.Column(main_placeholder, modal_window),
        favicon="static/icon/favicon.ico"
    )

create_app().servable()
