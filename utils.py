from imports import *
from config import *


def convert_datetime(obj):
    """Converts the datetime object to a string."""
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def create_dirs(terminal):
    """Creates the necessary directories for data storage."""
    dir_ls = [cache_dir, data_dir, img_dir, gif_dir, vid_dir, json_dir]

    log_to_terminal(terminal, console_msg.dir_create_msg)
    for directory in dir_ls:
        if not os.path.exists(directory):
            os.makedirs(directory)
            log_to_terminal(terminal, console_msg.dir_created.format(directory=directory))
        else:
            log_to_terminal(terminal, console_msg.dir_exists.format(directory=directory))


def create_movie_file(terminal):
    """Creates a movie from the images in the img_arr."""
    log_to_terminal(terminal, console_msg.vid_create_msg)
    file_str = ", ".join(map(str, img_arr))
    hash_obj = hashlib.md5(file_str.encode()).hexdigest()
    file_name = f'{vid_dir}/{hash_obj}.webp'
    file_name2 = f'{vid_dir}/{hash_obj}.mp4'

    if os.path.exists(file_name):
        # log_to_terminal(terminal, console_msg.vid_file_exists(file_name=file_name))
        return
    else:
        frames = [Image.open(img_path) for img_path in img_arr]
        imageio.mimsave(file_name2, frames, 'MP4', fps=2)


def create_animation_file(terminal):
    """Creates a movie from the images in the img_arr."""
    log_to_terminal(terminal, console_msg.vid_create_msg)
    file_str = ", ".join(map(str, img_arr))
    hash_obj = hashlib.md5(file_str.encode()).hexdigest()
    file_name = f'{vid_dir}/{hash_obj}.mp4'

    if os.path.exists(file_name):
        # log_to_terminal(terminal, console_msg.vid_file_exists(file_name=file_name))
        return
    else:
        frames = [Image.open(img_path) for img_path in img_arr]
        frames[0].save(
            file_name,
            save_all=True,
            append_images=frames[1:],
            duration=200,
            loop=0
        )

    log_to_terminal(terminal, console_msg.export_vid_success.format(file_name=file_name))



def clean_dt_values(dt_obj):
    """Cleans the datetime values for year, day, hour, and minute."""
    yr = dt_obj.year
    dy = dt_obj.timetuple().tm_yday
    hr = dt_obj.hour
    mn = dt_obj.minute
    return yr, dy, hr, mn


def fix_dt_values(start_time, end_time):
    """Fixes the datetime values for the start and end times."""
    current_time = datetime.now(timezone.utc)
    end_time = end_time.replace(tzinfo=timezone.utc)

    if abs(current_time - end_time) <= timedelta(minutes=5) and end_time.minute < 5 and main_dict['domain'] == 'C':
        print("Extending end time by 6 minutes to locate files...")
        start_time = start_time - timedelta(minutes=6)
        end_time = end_time - timedelta(minutes=6)

    return start_time, end_time


def get_composites(sat_data, value):
    for item in sat_data:
        if item.get("id") == value:
            return [composite["name"] for composite in item.get("composites", [])]
    return []


def log_to_terminal(terminal, message_template, **kwargs):
    """Logs a truncated message to the given terminal and scrolls to the bottom."""
    if terminal:
        message = message_template.format(**kwargs)
        truncated_message = message[:45] + '...' if len(message) > 45 else message
        terminal.write(f'\n{truncated_message}')


def clear_terminal(terminal):
    """Clears the terminal and logs a message."""
    if terminal:
        terminal.write('\nTerminal cleared...')
        terminal.clear()


def get_json_data(file_path):
    """Reads the JSON data from the given file path."""
    with open(file_path) as f:
        data = json.load(f)
    return data

def export_json_file(terminal):
    log_to_terminal(terminal, console_msg.export_json)
    processed_dict = convert_datetime(main_dict)
    file_name = f"{json_dir}/settings_export.json"
    with open(file_name, 'w') as file:
        json.dump(processed_dict, file, indent=4)
    log_to_terminal(terminal, console_msg.export_json_success.format(file_name=file_name))

def backup_json_file(terminal):
    log_to_terminal(terminal, console_msg.export_json)
    processed_dict = convert_datetime(main_dict)
    file_name = f"{json_dir}/settings_backup.json"
    with open(file_name, 'w') as file:
        json.dump(processed_dict, file, indent=4)


def hash_file_name(scan_time_stamp):
    """Hashes the file name using the scan time stamp."""
    def stringify(value):
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, list):
            return ','.join(map(str, value))
        else:
            return str(value)
    
    str_values = ''.join(stringify(value) for value in list(main_dict.values())[3:])
    conc_values = ''.join([scan_time_stamp, str_values])

    hash_obj = hashlib.md5(conc_values.encode())

    return hash_obj.hexdigest()


def import_json_file(sidebar, loc_data, prd_data, prj_data, sat_data):
    """Imports the JSON file and updates the sidebar."""
    json_file = sidebar[1][3][3].value
    data = json_file.decode('utf-8')
    data = json.loads(data)

    start_dt = datetime.fromisoformat(data['start_time'])
    end_dt = datetime.fromisoformat(data['end_time'])  
    sidebar[1][0][0].value = start_dt
    sidebar[1][0][1].value = end_dt
    sidebar[1][1][0].value = next((item['id'] for item in sat_data if item['bucket'] == data['bucket']), None)
    sidebar[1][1][1].value = {'C': 'CONUS', 'F': 'Full Disk'}.get(data['domain'], sidebar[1][1][1].value)
    sidebar[1][1][2].value = next((item['name'] for item in prj_data if item['id'] == data['projection']), None)
    sidebar[1][0][2].value = next((item['name'] for item in prd_data if item['id'] == data['composite']), None)
    sidebar[1][1][3][1].value = str(data['lat1'])
    sidebar[1][1][3][0].value = str(data['lat2'])
    sidebar[1][1][4][1].value = str(data['lon2'])
    sidebar[1][1][4][0].value = str(data['lon1'])
    sidebar[1][1][5][1][2].value = data['lat_lon_label']
    sidebar[1][1][5][1][0].value = data['state_borders']
    sidebar[1][1][5][1][1].value = data['water_borders']
    sidebar[1][1][5][3][2].value = data['lat_lon_grid']
    sidebar[1][1][5][3][0].value = data['country_borders']
    sidebar[1][1][5][3][1].value = data['county_borders']
    sidebar[1][1][6][0].value = data['border_color']
    sidebar[1][1][6][1].value  = data['border_width']




def test_print():
    """Test print the main_dict."""
    for item in main_dict:
        print(item, main_dict[item])

