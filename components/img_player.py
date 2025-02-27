from imports import *
from config import *
from utils import *

def create_img_player():
    """Creates the image player widget."""
    
    # Assuming img_arr contains URLs or file paths to images
    urls = [pn.pane.WebP(img, sizing_mode='scale_width') for img in img_arr]

    # Create tabs for images
    tabs = pn.Tabs(*[(str(scan_time), img) for scan_time, img in zip(dt_arr, urls)], align="center")
    
    return tabs, urls
