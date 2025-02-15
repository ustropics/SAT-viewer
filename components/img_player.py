from imports import *
from config import *
from utils import *

def create_img_player():
    """Creates the image player widget."""

    # Assuming img_arr contains URLs or file paths to images
    urls = [pn.pane.WebP(img, sizing_mode='scale_width') for img in img_arr]

    # Create tabs for images
    tabs = pn.Tabs(*[(f"Image {i}", img) for i, img in enumerate(urls)], align="center")

    # Create a player widget
    player = pn.widgets.Player(
        name='Player',
        start=0,
        end=len(urls) - 1,
        value=0,
        loop_policy='loop',
        interval=340,
        align='center'
    )

    # Link player to tabs
    player.jslink(tabs, value='active', bidirectional=True)

    # Combine tabs and player
    img_player = pn.Column(player, tabs)

    return img_player
