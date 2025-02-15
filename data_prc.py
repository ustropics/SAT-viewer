from imports import *
from config import *
from utils import *


# Create the main dictionary to store user input
def create_main_dict(sidebar, loc_data, prd_data, prj_data, sat_data):
    start_time                  = sidebar[1][0][0].value
    end_time                    = sidebar[1][0][1].value
    bucket                      = get_bucket(sidebar, loc_data, sat_data)
    composite                   = get_composite(sidebar, prd_data)
    domain                      = get_domain(sidebar, loc_data)
    reader                      = get_reader(bucket, sat_data)   

    location                    = get_location(sidebar)
    satellite                   = sidebar[1][1][0].value 
    projection                  = get_projection(sidebar, loc_data, prj_data)
    extent                      = get_extent(location)
    lat1, lat2, lon1, lon2      = get_lat_lon(extent, sidebar)

    lat_lon_label               = sidebar[1][1][5][1][2].value
    state_borders               = sidebar[1][1][5][1][0].value
    water_borders               = sidebar[1][1][5][1][1].value
    lat_lon_grid                = sidebar[1][1][5][3][2].value
    country_borders             = sidebar[1][1][5][3][0].value
    county_borders              = sidebar[1][1][5][3][1].value
    border_color                = sidebar[1][1][6][0].value
    border_width                = sidebar[1][1][6][1].value
    images                      = img_arr         

    main_dict['start_time']     = start_time
    main_dict['end_time']       = end_time
    main_dict['images']         = images
    main_dict['extent']         = extent
    main_dict['bucket']         = bucket
    main_dict['composite']      = composite
    main_dict['domain']         = domain
    main_dict['location']       = location
    main_dict['projection']     = projection
    main_dict['satellite']      = satellite
    main_dict['reader']         = reader
    main_dict['lat1']           = lat1
    main_dict['lat2']           = lat2
    main_dict['lon1']           = lon1
    main_dict['lon2']           = lon2
    main_dict['lat_lon_label']  = lat_lon_label
    main_dict['state_borders']  = state_borders
    main_dict['water_borders']  = water_borders
    main_dict['lat_lon_grid']   = lat_lon_grid
    main_dict['country_borders']= country_borders
    main_dict['county_borders'] = county_borders
    main_dict['border_color']   = border_color
    main_dict['border_width']   = border_width


# Function to get the bucket from satellite selection
def get_bucket(sidebar, loc_data, sat_data):

    satellite = sidebar[1][1][0].value

    if satellite == 'Autoselect':
        location = sidebar[1][0][3].value
        loc = next((item for item in loc_data if item["location"] == location), None)
        
        satellite = loc['satellite']
        sat = next((item for item in sat_data if item["name"] == satellite), None)

        sat_bucket = sat['bucket']
    else:
        sat = next((item for item in sat_data if item["id"] == satellite), None)
        sat_bucket = sat['bucket']

    return sat_bucket


# Function to get the composite id from user input
def get_composite(sidebar, prd_data):
    composite = sidebar[1][0][2].value
    comp = next((item for item in prd_data if item["name"] == composite), None)

    return comp['id']


# Function to get the domain id from user input
def get_domain(sidebar, loc_data):

    domain = sidebar[1][1][1].value

    if domain == 'Autoselect':
        location = sidebar[1][0][3].value
        loc = next((item for item in loc_data if item["location"] == location), None)
        domain_id = loc['domain']

    elif domain == 'CONUS':
        domain_id = 'C'

    elif domain == 'Full Disk':
        domain_id = 'F'

    return domain_id


# Function to get extent from location json file
def get_extent(location):
    data = get_json_data(location_data)

    for entry in data:
        if entry['location'] == location:
            return entry['extent']
    return None


# Check if user input lat/lon values, otherwise use loc values
def get_lat_lon(extent, sidebar):

    sb_lat1 = int(sidebar[1][1][3][1].value)
    sb_lat2 = int(sidebar[1][1][3][0].value)


    sb_lon1 = int(sidebar[1][1][4][0].value)
    sb_lon2 = int(sidebar[1][1][4][1].value)

    if sb_lat1 == 0 and sb_lat2 == 0 and sb_lon1 == 0 and sb_lon2 == 0:
        lat1 = extent[2]
        lat2 = extent[3]
        lon1 = extent[0]
        lon2 = extent[1]
    else:
        lat1 = sb_lat1
        lat2 = sb_lat2
        lon1 = sb_lon1
        lon2 = sb_lon2

    return lat1, lat2, lon1, lon2

def get_location(sidebar):
    location = sidebar[1][0][3].value

    sb_lat1 = int(sidebar[1][1][3][0].value)
    sb_lat2 = int(sidebar[1][1][3][1].value)


    sb_lon1 = int(sidebar[1][1][4][0].value)
    sb_lon2 = int(sidebar[1][1][4][1].value)

    if sb_lat1 == 0 and sb_lat2 == 0 and sb_lon1 == 0 and sb_lon2 == 0:
        location = location
    else:
        location = 'Custom'

    return location


# Get the projection id from user input
def get_projection(sidebar, loc_data, prj_data):

    projection = sidebar[1][1][2].value

    if projection == 'Autoselect':
        location = sidebar[1][0][3].value
        loc = next((item for item in loc_data if item["location"] == location), None)
        projection = loc['projection']
        proj = next((item for item in prj_data if item["name"] == projection), None)
    else:
        proj = next((item for item in prj_data if item["name"] == projection), None)

    return proj['id']

# Get the satpy reader from the satellite bucket
def get_reader(bucket, sat_data):

    reader = next((item["reader"] for item in sat_data if item["bucket"] == bucket), None)
    return reader