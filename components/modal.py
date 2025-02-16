from imports import *
from static.css.styles import *

from data_prc import create_main_dict
from utils import export_json_file, create_movie_file, create_animation_file

# Define the modal components
download_modal = pn.Column()
modal_window = pn.Modal(download_modal, width=400)

# Function to handle export button click
def json_btn_fnc(event, sidebar, loc_data, prd_data, prj_data, sat_data, terminal):

    # Create the main dictionary and export the JSON file
    create_main_dict(sidebar, loc_data, prd_data, prj_data, sat_data)
    file_name = export_json_file(terminal)

    # Create the file download button
    download_button = pn.widgets.FileDownload(
        filename="satviewer_settings.json",
        file=file_name,
        button_type="primary",
        label="Download JSON File",
        width=340,
    )

    text = pn.pane.Markdown(
        f"""
        File successfully exported as: </br>**satviewer_settings.json**.
        """,
        styles={
            'font-size': "14px",
            'color': theme_settings['dark_font'],
        }
    )

    container = pn.Column(text, download_button)

    # Update the modal window with the download button
    download_modal.clear()
    download_modal.append(container)
    modal_window.open = True

def movie_btn_fnc(event, terminal):
    print("event")
    """Handles the video creation and updates the modal window with a download button."""
    file_name = create_movie_file(terminal)
    
    if not file_name:
        text = pn.pane.Markdown(
            "⚠️ No video created. Please ensure images are available.",
            styles={'font-size': "14px", 'color': "red"}
        )
        container = pn.Column(text)
    else:
        download_button = pn.widgets.FileDownload(
            filename="satviewer_video.mp4",
            file=file_name,
            button_type="primary",
            label="Download Video File",
            width=340,
        )

        text = pn.pane.Markdown(
            f"Video successfully created as: </br>**satviewer_video.mp4**.",
            styles={'font-size': "14px", 'color': theme_settings['dark_font']}
        )

        container = pn.Column(text, download_button)

    # Update modal window with download button
    download_modal.clear()
    download_modal.append(container)
    modal_window.open = True


# Export modal components
__all__ = ["download_modal", "modal_window", "json_btn_fnc"]
