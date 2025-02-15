from imports import *
from config import *
from utils import *

from static.css.styles import *

def create_projection_info(value, prj_data):

    proj = next((item for item in prj_data if item["name"] == value), None)

    proj_image = pn.pane.PNG(
        f"static/image/{proj['id']}.png",
        sizing_mode='scale_width'
        )
    
    title = pn.pane.Markdown(
        f'# {proj["name"]}',
        styles={
            'text-align': "center",
            'background-color': theme_settings['primary_bg_color']
        },
        align='center',
        sizing_mode='scale_width'
    )

    description = pn.pane.Markdown(
        f'## {proj["header"]}\n' + proj['description'],
        styles={'font-size': "14px"},
        sizing_mode='scale_width'
    )

    bp_list = pn.pane.Markdown(
        f'## Description\n- {proj["bp1"]}\n- {proj["bp2"]}\n- {proj["bp3"]}',
        styles={'font-size': "14px"},
        sizing_mode='scale_width'
        )

    proj_area = pn.pane.Markdown(
        f'## Distortion\n' + proj['distortion'],
        styles={'font-size': "14px"},
        sizing_mode='scale_width'
    )

    image_container = pn.Column(proj_image)
    description_container = pn.Column(description, bp_list, proj_area)

    row1 = pn.Row(title, align='center', sizing_mode='scale_width')
    row2 = pn.Row(description_container, image_container)

    main_container = pn.Column(row1, row2)

    return main_container