from imports import *
from config import *
from utils import *
from static.certs import keys

def get_required_band_numbers(sat_data):
    composite = main_dict['composite']
    bucket = main_dict['bucket']

    for sat in sat_data:
        if sat['bucket'] == bucket:
            for comp in sat['composites']:
                if comp['id'] == composite:
                    return comp['bands']
            return bucket, None
    return None, None

def get_files_in_time_range(terminal, fs, start_time, end_time, sat_data):
    """Get data files in the specified time range."""
    domain = main_dict['domain']
    product_name = f'ABI-L1b-Rad{domain}'
    bucket_name = main_dict['bucket']

    # Get the required band numbers from the parsed data
    required_bands = get_required_band_numbers(sat_data)
    band_keywords = [f"C{str(band).zfill(2)}" for band in required_bands]


    # start_time = datetime(2025, 2, 11, 23, 50, 0)
    # end_time = datetime(2025, 2, 12, 0, 10, 0)


    start_time, end_time = fix_dt_values(start_time, end_time)
    start_yr, start_dy, start_hr, start_mn = clean_dt_values(start_time)
    end_yr, end_dy, end_hr, end_mn = clean_dt_values(end_time)
    files = []

    log_to_terminal(terminal, console_msg.dt_get_msg)
    log_to_terminal(terminal, console_msg.dt_start.format(start_time=start_time.strftime('%B {day}, %Y at %H:%M UTC').format(day=start_time.day)))
    log_to_terminal(terminal, console_msg.dt_end.format(end_time=end_time.strftime('%B {day}, %Y at %H:%M UTC').format(day=end_time.day)))
    log_to_terminal(terminal, console_msg.server_connect_msg.format(bucket_name=bucket_name))
    log_to_terminal(terminal, console_msg.server_url.format(server=server))


    if start_dy == end_dy:
        for hr in range(start_hr, end_hr + 1):
            files.extend(fs.ls(f'{bucket_name}/{product_name}/{start_yr}/{start_dy:03.0f}/{hr:02.0f}'))
    else:
        files.extend(fs.ls(f'{bucket_name}/{product_name}/{start_yr}/{start_dy:03.0f}/{start_hr:02.0f}'))
        files.extend(fs.ls(f'{bucket_name}/{product_name}/{end_yr}/{end_dy:03.0f}/{end_hr:02.0f}'))


    return [
        file for file in files if any(keyword in str(file) for keyword in band_keywords) and
        is_within_time_range(parse_file_timestamp(file), start_time, end_time)
    ]

def is_within_time_range(timestamp, start_time, end_time):
    """Check if timestamp is within the range."""
    return start_time.replace(tzinfo=timezone.utc) <= timestamp.replace(tzinfo=timezone.utc) <= end_time.replace(tzinfo=timezone.utc)

def parse_file_timestamp(file):
    """Parse timestamp from file name."""
    timestamp_str = file.split('_e')[1].split('_')[0]
    base_ts = datetime(int(timestamp_str[:4]), 1, 1)
    return base_ts + timedelta(days=int(timestamp_str[4:7]) - 1, hours=int(timestamp_str[7:9]), minutes=int(timestamp_str[9:11]), seconds=int(timestamp_str[11:13]))

def round_dt_minute(dt):
    # Calculate how many minutes to add/subtract
    minutes = (dt.minute + 5) // 10 * 10
    rounded_dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minutes)
    
    # Adjust if rounding pushes it to the next hour
    if minutes == 60:
        rounded_dt += timedelta(hours=1)
        rounded_dt = rounded_dt.replace(minute=0)
    
    return rounded_dt

def handle_file_status(terminal, file, band_files):
    """Handle file status: log whether it exists or needs to be downloaded."""
    # Construct the local file name
    file_name = data_dir + file.split("/")[-1]

    # Extract the band ID based on the "_M6" identifier
    try:
        band_id = file.split("-M6C")[1][:2]  # Get the two characters after "_M6"
    except IndexError:
        log_to_terminal(terminal, f"Error: Unable to extract band ID from file: {file}")
        return None

    # Check if the file exists and log accordingly
    if os.path.exists(file_name):
        emoji = f"Band {band_id}"
        log_to_terminal(terminal, console_msg.file_exists.format(emoji=emoji, file_name=file_name))
    else:
        emoji = f"Band {band_id}"
        log_to_terminal(terminal, console_msg.file_dl.format(emoji=emoji, file_name=file_name))

    # Add the file to the band_files dictionary
    band_files.setdefault(band_id, []).append(file_name)

    return file_name

def handle_file_download(file, fs):
    """Download the file if it does not exist locally."""
    file_name = data_dir + file.split("/")[-1]
    fs.download(file, file_name)

def get_data_files_goes(terminal, sat_data):
    """Main function to get data files for GOES satellite."""
    band_files = {}

    # Get files in time range
    files = get_files_in_time_range(terminal, fs, main_dict['start_time'], main_dict['end_time'], sat_data)

    log_to_terminal(terminal, console_msg.file_found.format(files=len(files)))

    # Filter files that need to be downloaded
    files_to_download = []
    
    for file in files:
        file_path = handle_file_status(terminal, file, band_files)
        if file_path and not os.path.exists(file_path):  # Check existence before adding to download list
            files_to_download.append(file)

    # Use ThreadPoolExecutor to download only missing files
    if files_to_download:
        with ThreadPoolExecutor() as executor:
            executor.map(lambda f: handle_file_download(f, fs), files_to_download)

    return band_files


def get_data_files_hima(terminal, sat_data):
    bucket_url = main_dict['bucket']
    prefix_base = 'AHI-L1b-FLDK'
    band_nums = get_required_band_numbers(sat_data)
    band_array = [f'B{num:02d}' for num in band_nums]


    start_time = round_dt_minute(main_dict['start_time']) - timedelta(minutes=20)
    end_time = round_dt_minute(main_dict['end_time']) - timedelta(minutes=20)

    log_to_terminal(terminal, console_msg.dt_get_msg)
    log_to_terminal(terminal, console_msg.dt_start.format(start_time=start_time.strftime('%B {day}, %Y at %H:%M UTC').format(day=start_time.day)))
    log_to_terminal(terminal, console_msg.dt_end.format(end_time=end_time.strftime('%B {day}, %Y at %H:%M UTC').format(day=end_time.day)))
    log_to_terminal(terminal, console_msg.server_connect_msg.format(bucket_name=bucket_url))
    log_to_terminal(terminal, console_msg.server_url.format(server=server))


    base_local_dir = data_dir
    fs = s3fs.S3FileSystem(anon=True)

    def generate_time_intervals(start, end, delta=timedelta(minutes=10)):
        """Generate time intervals in 10-minute increments."""
        current = start
        while current <= end:
            yield current
            current += delta

    def download_file(s3_path, local_path):
        """Download a single file from S3."""
        fs.get(s3_path, local_path)
        return local_path

    # Collect all files to download and their respective directories
    files_to_download = []
    directories = []

    for time_point in generate_time_intervals(start_time, end_time):
        date_str = time_point.strftime('%Y/%m/%d')
        time_str = time_point.strftime('%H%M')
        
        dt_prefix = f'{date_str}/{time_str}/'
        s3_prefix = f'{prefix_base}/{dt_prefix}'
        local_dir = os.path.join(base_local_dir, date_str, time_str)
        os.makedirs(local_dir, exist_ok=True)
        directories.append(dt_prefix)
        
        try:
            files = fs.ls(f'{bucket_url}/{s3_prefix}')
        except FileNotFoundError:
            print(f'No files found for {time_point}')
            continue

        # Filter files by bands
        for file in files:
            if any(band in file for band in band_array):
                local_path = os.path.join(local_dir, os.path.basename(file))
                if not os.path.exists(local_path):  # Check if file exists locally
                    log_to_terminal(terminal, console_msg.file_dl.format(emoji='', file_name=local_path))
                    files_to_download.append((file, local_path))
                else:
                    print(f'Skipping download, file already exists: {local_path}')
                    log_to_terminal(terminal, console_msg.file_exists.format(emoji='', file_name=local_path))

    # Download files concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(download_file, file, path): file for file, path in files_to_download}
        for future in as_completed(future_to_file):
            filename = os.path.basename(future_to_file[future])
            try:
                future.result()
                print(f'Downloaded: {filename}')
            except Exception as e:
                print(f'Error downloading {filename}: {e}')

    print('Download complete.')
    print('Directories created:', directories)
    return directories

def get_data_files_mtl1(terminal, sat_data):
    """Get data files for MTI-1 satellite."""

    credentials = (keys.consumer_key, keys.consumer_secret)

    # start_time = '2025-02-22T22:30:00'
    # end_time = '2025-02-22T22:50:00'
    start_time = round_dt_minute(main_dict['start_time']) - timedelta(minutes=10)
    end_time = round_dt_minute(main_dict['end_time'])

    start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S')
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S')

    # Authenticate
    token = eumdac.AccessToken(credentials)
    # print(f"This token '{token}' expires {token.expiration}")

    # Connect to the datastore
    datastore = eumdac.DataStore(token)
    sub_dirs = []  # Initialize an empty list to store sub_dir values

    # Perform search
    search_results = list(datastore.opensearch(f"pi=EO:EUM:DAT:0665&dtstart={start_time}&dtend={end_time}"))
    search_results_hd = list(datastore.opensearch(f"pi=EO:EUM:DAT:0662&dtstart={start_time}&dtend={end_time}"))
    
    all_results = search_results + search_results_hd
    
    # Check if there are results
    if not all_results:
        print("No results found for the given time range.")
    else:
        print(f"Found {len(all_results)} results.")

        # Loop through search results and download each file
        for product in all_results:
            print(f"Processing: {product}")
            print(dir(product))

            satellite = product.satellite
            timestamp = product.sensing_end

            formatted_time = timestamp.strftime("%Y%m%d%H%M")
            sub_dir = f'data/{satellite}/{formatted_time}'

            # Create the sub_dir if it doesn't exist
            os.makedirs(sub_dir, exist_ok=True)

            # Append the sub_dir to the list
            sub_dirs.append(sub_dir)

            # Extract filename from URL and clean it
            url_filename = os.path.basename(product.url)  # Use product.location instead of product.url
            local_filename = urllib.parse.unquote(url_filename.split("?")[0])  # Decode and remove query params

            local_filename += ".zip"  # Add .zip extension   
            local_filepath = os.path.join(sub_dir, local_filename)  # Save file in sub_dir

            # Check if file already exists
            if os.path.exists(local_filepath):
                print(f"File already exists: {local_filepath}, skipping download.")
                extract_nc_files(local_filepath, sub_dir)
                continue  # Skip downloading if file exists

            # Open product for download
            with product.open() as remote_file:
                with open(local_filepath, 'wb') as local_file:
                    shutil.copyfileobj(remote_file, local_file)

            print(f"Downloaded {local_filepath}")
            extract_nc_files(local_filepath, sub_dir)

    return sub_dirs  # Return the list of sub_dirs