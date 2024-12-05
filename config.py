from imports import *

# Temporary buck and product names for s3fs
bucket_name = 'noaa-goes16'
product_name = 'ABI-L1b-RadC'

# Create empty dictionaries and lists to hold values
main_dict = {}

# Directories that need to be created
cache_dir = 'cache/'
data_dir = 'data/'
img_dir = 'media/'

# Initial datetime values for the datetime pickers (use current time and 10 min delta)
init_dt = datetime.now(timezone.utc).replace(second=0, microsecond=0)
init_os = init_dt - timedelta(minutes=10)

# Initialize the S3 filesystem
fs = s3fs.S3FileSystem(anon=True)