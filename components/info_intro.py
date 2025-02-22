from imports import *
from config import *
from utils import *

from static.css.styles import *

def create_intro_info(sidebar, prd_data):

    # Get the selected composite
    composite = sidebar[1][0][2].value
    comp = next((item['id'] for item in prd_data if item["name"] == composite), None)

    # Create the main title
    title = pn.pane.Markdown(
        f'# SAT-Viewer (version 1.2)',
        styles={
            'text-align': "center",
            'background-color': theme_settings['primary_bg_color']
        },
        align='center',
        sizing_mode='scale_width'
    )

    # Load in the composite image
    comp_image = pn.pane.PNG(
        f"static/image/{comp}.png",
        sizing_mode='scale_width'
        )

    # Create the main description
    description = pn.pane.Markdown(
        f"""
        ## Creating High-Quality Satellite Imagery
        SAT-Viewer is a web application designed for generating high-quality, true-resolution satellite imagery with advanced correction and processing options. It streamlines the workflow for handling satellite data, ensuring accurate, visually enhanced outputs.
        </br></br>
        The platform automatically downloads the required band data for available composites, applies necessary corrections—including atmospheric and Rayleigh scattering adjustments—and can upsample specific bands to a true resolution of 500m per pixel. SAT-Viewer supports multiple satellite sensors and projection methods, making it a versatile tool for researchers, meteorologists, and remote sensing professionals.</br>
        """,
        styles={'font-size': "14px"},
        sizing_mode='scale_width'
        )

    # Create the main features    
    features = pn.pane.Markdown(
        f"""
        ### Key Features</br>
        - <b>Rayleigh Correction</b>: Removes atmospheric scattering effects to improve image clarity
        - <b>Solar Zenith Angle Adjustment</b>: Accounts for sun angle variations to enhance brightness consistency
        - <b>Resolution Upsampling</b>: Merges lower-resolution bands with higher-resolution channels
        - <b>Support for Multiple Sensors</b>: Compatible with GOES and Himawari instruments (polar orbitting in pipeline)
        """,
        styles={
            'font-size': "14px",
            'background-color': theme_settings['secondary_color'],
            'color': theme_settings['dark_font'],
            'padding': '10px',
            },
        sizing_mode='scale_width'
    )

    # Create the version information
    version = pn.pane.Markdown(
        f"""
        ### Version 1.2
        - SAT-Viewer is now accessible via dedicated server and DNS URL at http://satviewer.com
        - Added support for Himawari-8 and Himawari-9 satellite data
        - Added support for GOES-19 and GOES-17 satellite data
        - Integrated with NGINX server for improved data handling
        - Ability to export settings as a JSON file for later use
        """,
        styles={
            'font-size': "14px",
            'padding': '10px',
            'background-color': theme_settings['warning_bg_color']
            },
        sizing_mode='scale_width'
    )

    # Create the quick start guide
    quick_start = pn.pane.Markdown(
        f"""
        ### Quick Start
        1. Select a satellite composite from the menu on the left.
        2. Choose a time range using the start and end date pickers.
        3. Select a location from the dropdown menu.
        4. Just hit Run to generate the composite images!
        5. After the images are generated, a media player will appear to view the images.
        """,
        styles={
            'font-size': "14px",
            },
        sizing_mode='scale_width'
    )

    # Create the custom options guide
    custom_options = pn.pane.Markdown(
        f"""
        ### Customize your Product
        - **Satellite**: Choose between GOES or Himawari instruments.
        - **Location**: Make your own extent with lat/lon coordinates.
        - **Projection**: Choose from various map projections.
        - **Export**: Save your set options as a json file and import them later.
        - **Media**: Save the generated composite as an mp4, animated image, or separate frames.
        """,
        styles={
            'font-size': "14px",
            },
        sizing_mode='scale_width'
    )

    # Create the additional information
    additional_info = pn.pane.Markdown(
        f"""
        ### Additional Information
        SAT-Viewer is optimized for performance and scalability, enabling easy custom composite creation. However, generating full-resolution RGB composites with corrections requires intensive processing, including advanced algorithms and resampling. As a result, rendering may take minutes per image.
        """,
        styles={
            'font-size': "14px",
            },
        sizing_mode='scale_width'
    )
    

    # Create the container layout
    col1 = pn.Column(description, features, version)
    row1 = pn.Row(col1, comp_image)
    row2 = pn.Row(quick_start, custom_options, additional_info)

    # Create the main container
    main_container = pn.Column(title, row1, row2)

    return main_container