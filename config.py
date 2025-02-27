from imports import *
from static.css.styles import *

# Temporary buck and product names for s3fs
server = 'https://registry.opendata.aws/noaa-goes/'

# Main app settings
app_settings = {    
    'console_output': 'disable',
    'design': 'material',
    'theme': 'dark',
    'raw_css': [css]
    } 

# Initialize the datetime objects and S$ filesystem
init_dt = datetime.now(timezone.utc).replace(second=0, microsecond=0)
init_os = init_dt - timedelta(minutes=10)
fs = s3fs.S3FileSystem(anon=True)

# Directories, dictionaries, and arrays that need to be created
cache_dir = 'cache/'
data_dir = 'data/'
gif_dir = 'media/gif/'
img_dir = 'media/img/'
vid_dir = 'media/vid/'
json_dir = 'media/json/'
main_dict = {}
img_arr = []
dt_arr = []
sat_version = '0.5'

# Data file locations
location_data = 'static/json/location_data.json'
product_data = 'static/json/product_data.json'
satellite_data = 'static/json/satellite_data.json'
projection_data = 'static/json/projection_data.json'

# Global variables
show_tooltip = 0


# Console messages
console_msg = SimpleNamespace(
    dask_init_msg = '\n🚀  Dask client initialized:',
    dir_create_msg = '\n📂  Creating directories:',
    dir_created = '{directory} created.',
    dir_exists = '{directory} already exists.',
    dt_get_msg = '\n🕒  Getting data files from:',
    dt_start = '{start_time} to',
    dt_end = '{end_time}...\n',
    export_json = 'Exporting JSON file...',
    export_json_success = '{file_name} exported successfully!',
    export_vid_success = '{file_name} created successfully!',
    file_complete = '\n💾  Download complete:',  
    file_dl = '  {emoji}  Downloading: {file_name}...',
    file_exists = '  {emoji}  File Exists: {file_name}...',
    file_found = '🔍  Total files found: {files}',
    file_total = 'Total files downloaded: {files}',
    img_file_exists = 'Image file exists...',
    program_init_msg = '🌎  Program initialized...',
    program_welcome_msg = f'Welcome to SAT-viewer v{sat_version}!',
    product_create_msg = '\n📊  Creating product:',
    product_recipe = 'Composite: {recipe}',
    projection_recipe = 'Projection: {projection}',
    scene_process_msg = '\n🗺️  Processing files for scene {scene}',
    server_connect_msg = '🖥️  Connecting to {bucket_name} data server...',
    server_url = '{server}\n',
    vid_create_msg = '\n🎥  Creating video...',
    vid_file_exists = 'Video file exists: {file_name}',
    vid_file_name = 'Video saved as: {file_name}'

)