from imports import *
from config import *
from utils import *

def get_time_range_values():
    """Gets the time range from the main_dict."""
    start_yr, start_dy, start_hr, start_mn = clean_dt_values(main_dict['start_time'])
    end_yr, end_dy, end_hr, end_mn = clean_dt_values(main_dict['end_time'])

    return start_yr, start_dy, start_hr, start_mn, end_yr, end_dy, end_hr, end_mn


def list_files_in_time_range(fs, bucket_name, product_name, start_yr, start_dy, start_hr, end_yr, end_dy, end_hr):
    """List all files in the given time range."""
    files = []
    if start_dy == end_dy and start_hr == end_hr:
        files = fs.ls(f'{bucket_name}/{product_name}/{end_yr}/{end_dy:03.0f}/{end_hr:02.0f}')
    else:
        for hr in range(start_hr, end_hr + 1):
            files.extend(fs.ls(f'{bucket_name}/{product_name}/{start_yr}/{start_dy:03.0f}/{hr:02.0f}'))
    
    return files


def filter_files_by_content(files, keywords):
    """Filter files that contain specific substrings."""
    return [file for file in files if any(keyword in str(file) for keyword in keywords)]


def parse_file_timestamp(file):
    """Extract and parse the timestamp from the file name."""
    timestamp_str = file.split('_e')[1].split('_')[0]
    year = int(timestamp_str[:4])
    day_of_year = int(timestamp_str[4:7])
    hour = int(timestamp_str[7:9])
    minute = int(timestamp_str[9:11])
    second = int(timestamp_str[11:13])

    base_ts = datetime(year, 1, 1)  # Start with January 1st of the given year
    return base_ts + timedelta(days=day_of_year - 1, hours=hour, minutes=minute, seconds=second)


def is_within_time_range(timestamp, start_time, end_time):
    """Check if a timestamp is within the specified time range."""
    utc_timestamp = timestamp.replace(tzinfo=timezone.utc)
    return start_time.replace(tzinfo=timezone.utc) <= utc_timestamp <= end_time.replace(tzinfo=timezone.utc)


def get_data_files(terminal):
    """Main function to get the data files."""

    # Get time range
    start_yr, start_dy, start_hr, start_mn, end_yr, end_dy, end_hr, end_mn = get_time_range_values()


    # Format the dt range to print to terminal
    start_dt = main_dict['start_time']
    end_dt = main_dict['end_time']

    start_dt_frmtd = start_dt.strftime("%B {day}, %Y at %H:%M UTC").format(day=start_dt.day)
    end_dt_frmtd = end_dt.strftime("%B {day}, %Y at %H:%M UTC").format(day=end_dt.day)

    log_to_terminal(terminal, f"\nGetting data files from:\n{start_dt_frmtd} to\n{end_dt_frmtd}...\n")

    # List files in the time range
    files = list_files_in_time_range(fs, bucket_name, product_name, start_yr, start_dy, start_hr, end_yr, end_dy, end_hr)

    # Filter files by content
    relevant_files = filter_files_by_content(files, ["C01", "C02", "C03"])

    # Further filter files by timestamp
    file_ls = []
    for file in relevant_files:
        timestamp = parse_file_timestamp(file)
        if is_within_time_range(timestamp, main_dict['start_time'], main_dict['end_time']):
            file_ls.append(file)

    total_files = f'Total files found: {len(file_ls)}\n'
    log_to_terminal(terminal, total_files)

        # Function to download a single file
    def download_file(file, fs):
        file_name = data_dir + file.split("/")[-1]
        if os.path.exists(file_name):
            log_to_terminal(terminal, f"💾 File exists: {file_name}")
            print(f"File exists: {file_name}\n\n")
        else:
            log_to_terminal(terminal, f'💾 Downloading {file_name}...')
            print(f'Downloading {file_name}...\n\n')
            fs.download(file, file_name)

    # Use ThreadPoolExecutor to download files concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: download_file(file, fs), file_ls)

    print(f'Download complete...{len(file_ls)} total files downloaded.')

