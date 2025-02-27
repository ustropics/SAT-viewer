from imports import *
from config import *
from utils import *

def create_product(sidebar, terminal, band_files):
    """
    Create a product using dynamically supplied band files.
    
    Args:
        sidebar: UI sidebar for user input and messages.
        terminal: Terminal for logging messages.
        band_files: A dictionary where keys are band IDs and values are lists of file paths.
    """
    start_fn_time = datetime.now()
    recipe = main_dict['composite']
    bucket = main_dict['bucket']

    log_to_terminal(terminal, console_msg.product_create_msg)
    log_to_terminal(terminal, console_msg.product_recipe.format(recipe=recipe))
    log_to_terminal(terminal, console_msg.projection_recipe.format(projection=main_dict['projection']))

    # Create the projection dictionary for the area definition
    proj_dict = {
        'proj': main_dict['projection'],
        'lat_0': 0.5 * (main_dict['lat1'] + main_dict['lat2']),
        'lon_0': 0.5 * (main_dict['lon1'] + main_dict['lon2']),
        'lat_1': main_dict['lat1'],
        'lat_2': main_dict['lat2'],
        'h': 35786023.0,
        'ellps': 'GRS80',
    }

    # Create the area definition in Satpy
    area_def = create_area_def(
        'projection_area',
        proj_dict,
        width=5000,
        height=5000,
        units='degrees',
        area_extent=[main_dict['lon1'], main_dict['lat1'], main_dict['lon2'], main_dict['lat2']],
    )

    # Dynamically determine the number of files to process
    if bucket == 'noaa-himawari9' or bucket == 'mti1':
        num_files = len(band_files)    
    else:
        num_files = len(next(iter(band_files.values())))
        band_ids = list(band_files.keys())  # Get the band IDs

    for i in range(num_files):
        log_to_terminal(terminal, console_msg.scene_process_msg.format(scene=i))

        if bucket == 'noaa-himawari9':
            scn_ls = glob(f'{data_dir}/{band_files[i]}/*.bz2')
            format_item = band_files[i].replace('/', '')
            format_time = datetime.strptime(format_item, '%Y%m%d%H%M')
            time_coverage_end = format_time.strftime('%Y-%m-%dT%H:%M:%S') + '.6Z'
            print(time_coverage_end)
        elif bucket == 'mti1':
            scn_ls = glob(f'{band_files[i]}/*.nc')
            format_item = band_files[i].split('/')[-1].split('_')[0]
            format_time = datetime.strptime(format_item, '%Y%m%d%H%M')
            time_coverage_end = format_time.strftime('%Y-%m-%dT%H:%M:%S') + '.6Z'
            print(time_coverage_end)
        else:
            print(f"band_files: {band_files}")
            print(f"band_ids: {band_ids}")
            print(f"indices: {[i for band_id in band_ids]}")
            scn_ls = [band_files[band_id][i] for band_id in band_ids]
            file_path = band_files[band_ids[0]][i]  # Use the first band to get the file path
            nc_file = xr.open_dataset(file_path, engine='netcdf4')
            time_coverage_end = nc_file.attrs.get('time_coverage_end')
            print(time_coverage_end)
        
        
        # Load the scene with necessary reader, filenames, and composite
        scn = Scene(reader=main_dict['reader'], filenames=scn_ls)

        # Run hash function to create a unique filename and append to array
        hash_name = hash_file_name(time_coverage_end)
        file_name = f'{img_dir}/{hash_name}.webp'
        img_arr.append(file_name)

        scn.load([recipe])
        if main_dict['location'] == 'CONUS' or main_dict['location'] == 'GLOBAL':
            new_scn = scn.resample(scn.max_area(), resampler='native')
        else:
            new_scn = scn.resample(area_def, resampler='nearest', cache_dir=cache_dir)


        if os.path.exists(file_name):
            log_to_terminal(terminal, console_msg.img_file_exists)
            scan_time = new_scn[recipe].attrs['end_time'].strftime("%b %d, %Y at %H:%M:%S")
            dt_time = new_scn[recipe].attrs['end_time'].strftime("%H:%M")
            dt_arr.append(dt_time)
            continue
        else:
            scn.load([recipe])
            scan_time = new_scn[recipe].attrs['end_time'].strftime("%b %d, %Y at %H:%M:%S")
            dt_time = new_scn[recipe].attrs['end_time'].strftime("%H:%M")
            dt_arr.append(dt_time)
            if main_dict['location'] == 'CONUS' or main_dict['location'] == 'GLOBAL':
                new_scn = scn.resample(scn.min_area(), resampler='native')
            else:
                new_scn = scn.resample(area_def, resampler='nearest', cache_dir=cache_dir)

            scan_time = new_scn[recipe].attrs['end_time'].strftime("%b %d, %Y at %H:%M:%S")
            sat_name = main_dict['satellite']

            area = new_scn[recipe].attrs['area']
            crs = area.to_cartopy_crs()
            file_title = f'{sat_name} {recipe} {scan_time}'

            try:
                y_val = new_scn[recipe].shape[1]
                x_val = new_scn[recipe].shape[2]
            except:
                y_val = new_scn[recipe].shape[0]
                x_val = new_scn[recipe].shape[1]


            if main_dict['location'] == 'GLOBAL' or main_dict['bucket'] == 'noaa-himawari9':
                y_in = 15
                x_in = 15
            else:
                # Convert to inches
                y_in = y_val / 333
                x_in = x_val / 333

            plt.figure(figsize=(x_in, y_in))
            ax = plt.axes(projection=crs)

            img = get_enhanced_image(new_scn[recipe])
            img_data = img.data

            if main_dict['lat_lon_grid']:
                gridlines = ax.gridlines(
                    draw_labels=main_dict['lat_lon_label'],
                    linewidth=0.8,
                    color='gray',
                    alpha=0.8,
                    linestyle='--',
                )
                if main_dict['lat_lon_label']:
                    gridlines.top_labels = False
                    gridlines.left_labels = False
                    gridlines.right_labels = True
                    gridlines.bottom_labels = True

            if main_dict['state_borders']:
                ax.add_feature(cfeature.STATES, edgecolor=main_dict['border_color'], linewidth=float(main_dict['border_width']))

            if main_dict['country_borders']:
                ax.add_feature(cfeature.BORDERS, edgecolor=main_dict['border_color'], linewidth=float(main_dict['border_width']))
                ax.add_feature(cfeature.COASTLINE, edgecolor=main_dict['border_color'], linewidth=float(main_dict['border_width']))

            if main_dict['water_borders']:
                ax.add_feature(cfeature.LAKES, edgecolor=main_dict['border_color'], linewidth=float(main_dict['border_width']))
                ax.add_feature(cfeature.RIVERS, edgecolor=main_dict['border_color'], linewidth=float(main_dict['border_width']))

            # Plot the image
            img_data.plot.imshow(ax=ax, vmin=0, vmax=1, rgb='bands')
            plt.rcParams["axes.titlesize"] = x_in - x_in/3
            plt.title(file_title)
            plt.savefig(file_name, dpi=800, bbox_inches='tight')
            plt.close()

    end_fn_time = datetime.now()
    total_fn_time = end_fn_time - start_fn_time

    log_to_terminal(terminal, f'Total time to create product: {total_fn_time}')
