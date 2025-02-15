from imports import *
from config import *
from utils import *

from static.css.styles import *


# Main function to create composite info pane
def create_composite_info(value, loc_data, prd_data, sat_data, sidebar):


    # Find the product and satellite data based on user value
    prod = next((item for item in prd_data if item["name"] == value), None)
    satellite = sidebar[1][1][0].value
    location = sidebar[1][0][3].value
    composite = sidebar[1][0][2].value

    comp = next((item['id'] for item in prd_data if item["name"] == composite), None)

    if satellite == 'Autoselect':
        loc = next((item for item in loc_data if item["location"] == location), None)

        satellite = loc['satellite']
        sat = next((item for item in sat_data if item["name"] == satellite), None)
    else:
        for item in sat_data:
            if item['id'] == satellite:
                sat = item
                break


    # Load in the composite image
    comp_image = pn.pane.PNG(
        f"static/image/{comp}.png",
        sizing_mode='scale_width'
        )

    # Create the title pane
    title = pn.pane.Markdown(
        f'# {prod["name"]} Information',
        styles={
            'text-align': "center",
            'background-color': theme_settings['primary_bg_color']
        },
        align='center',
        sizing_mode='scale_width'
    )

    # Create the description pane
    description = pn.pane.Markdown(
        f"## {prod['header']}\n" + prod['description'],
        styles={'font-size': "14px"},
        sizing_mode='scale_width'
    )

    true_comp_arr = ['true_color', 'true_color_reproduction_corr', 'cimss_true_color_sunz_rayleigh']
    
    if comp in true_comp_arr:
    # Create the bands pane
        bands = pn.pane.Markdown(
            f"""
            ### Bands for {sat['name']} and the {sat['instrument_name']} Instrument
            <table style="width:100%; border-color: {theme_settings['primary_bg_color']};">
            <tr>
            <td style="background-color: {theme_settings['primary_bg_color']}">Color</td>
            <td style="background-color: {theme_settings['primary_bg_color']}">Wavelength</td>

            </tr>
            <tr>
            <td><span style="color:{theme_settings['red_band_color']}">Red</span></td>
            <td><span>{prod['bands']['red']}</span></td>
            </tr>
            <tr>
            <td><span style="color:{theme_settings['green_band_color']}">Green</span></td>
            <td><span>{prod['bands']['green']}</span></td>
            </tr>
            <tr>
            <td><span style="color:{theme_settings['blue_band_color']}">Blue</span></td>
            <td><span>{prod['bands']['blue']}</span></td>
            </tr>
            </table>
            """,
            styles={'font-size': "14px"},
            sizing_mode='stretch_width'
        )

    elif comp == 'colorized_ir_clouds':
        bands = pn.pane.JPG('static/image/b13.jpg')

    else:    
        bands = pn.pane.Markdown(
            f"""
            ### Bands for {sat['name']} and the {sat['instrument_name']} Instrument
            <table style="width:100%; border-color: {theme_settings['primary_bg_color']};">
            <tr>
            <td style="background-color: {theme_settings['primary_bg_color']}">Band</td>
            <td style="background-color: {theme_settings['primary_bg_color']}">Wavelength</td>
            <td style="background-color: {theme_settings['primary_bg_color']}">Relates to</td>
            <td style="background-color: {theme_settings['primary_bg_color']}">Contribution</td>
            </tr>
            <tr>
            <td><span style="color:{theme_settings['red_band_color']}">Red</span></td>
            <td><span>{prod['bands']['red']}</span></td>
            <td><span>{prod['relates_to']['red']}</span></td>
            <td><span style="color:{theme_settings['red_band_color']}">{prod['contribution']['red']}</span></td>
            </tr>
            <tr>
            <td><span style="color:{theme_settings['green_band_color']}">Green</span></td>
            <td><span>{prod['bands']['green']}</span></td>
            <td><span>{prod['relates_to']['green']}</span></td>
            <td><span style="color:{theme_settings['green_band_color']}">{prod['contribution']['green']}</span></td>
            </tr>
            <tr>
            <td><span style="color:{theme_settings['blue_band_color']}">Blue</span></td>
            <td><span>{prod['bands']['blue']}</span></td>
            <td><span>{prod['relates_to']['blue']}</span></td>
            <td><span style="color:{theme_settings['blue_band_color']}">{prod['contribution']['blue']}</span></td>
            </tr>
            </table>
            """,
            styles={'font-size': "14px"},
            sizing_mode='stretch_width'
        )

    # Create the usage pane
    usage = pn.pane.Markdown(
        f"""
        ## Operation's Usage
        {prod['operation_usage']}
        """,
        sizing_mode='scale_width',
        styles={
            'font-size': "14px",
            'background-color': theme_settings['secondary_color'],
            'color': theme_settings['dark_font'],
            'padding': '10px',
            'height': '200px'
        }
    )

    # Create the corrections pane
    formatted_list = ", ".join(prod['corrections'])
    corrections = pn.pane.Markdown(
        f"""
        ### Corrections
        { formatted_list }
        """,
        styles={'font-size': "14px"}
    )

    # Create the limitations pane
    limit = pn.pane.Markdown(
        f"""
        ## Limitations
        {prod['operation_limitation']}
        """,
        sizing_mode='scale_width',
        styles={
            'font-size': "14px",
            'background-color': theme_settings['warning_bg_color'],
            'color': '#faf6f0',
            'padding': '10px',
            'height': '200px'
        }
    )


    # Create the containers and rows
    description_container = pn.Column(description, corrections, bands)
    image_container = pn.Column(comp_image)
    row1 = pn.Row(title, align='center', sizing_mode='scale_width')
    row2 = pn.Row(description_container, image_container)
    row3 = pn.Row(usage, limit)

    # Create the main container
    main_container = pn.Column(row1, row2, row3)

    return main_container