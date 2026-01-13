import os
import random
import sys
import time
import yaml
from datetime import timedelta
from tqdm import tqdm


from utils.audio_vessel_annotator import process_deployment_data, filter_date
from utils.distance_calculator import process_data
from utils.find_closest_wav import create_closest_ships

from utils.plot_spectrogram_distance import database_creater
from utils.data_processing_utils import (
    calculate_date_range,
    filter_dataframe_by_date,
    determine_data_location,
    filter_smoothed_data,
    process_data_samples,
)


from utils.import_data import (
    dict_id_to_station,
    hourly_intervals_date,
)

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Append the 'utils' directory relative to the script's location
utils_path = os.path.join(script_directory, 'utils')
sys.path.append(utils_path)

# Path to the config.yaml relative to the script's location
config_path = os.path.join(script_directory, 'config.yaml')
# Load configuration from YAML
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


config = load_config(config_path )
window = config.get("window", 6)
comment = config.get("comment", "subset_cmmi")
# Base paths from config
base_directory = config["paths"]["base_directory"]
csv_location = config["paths"]["csv_location"]
raw_data_folder=config["paths"]["raw_data_folder"]

plot_location_two = rf'plots_per_station_{window}_{comment}'
data_per_station = rf'data\data_per_station_{window}_{comment}'
csv_file_database = rf'database.csv'

# Set seed for reproducibility
random.seed(config['seed'])


# Main function to process deployments
def main():
    base_directory = config['paths']['base_directory']
    deployment_dirs = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

    print("{} [START] Looping over deployments".format(time.strftime("%H:%M:%S")))

    with tqdm(total=len(deployment_dirs), desc="{} [PROCESSING] Deployments".format(time.strftime("%H:%M:%S")),
              position=0, leave=True) as pbar:
        for deployment_id in deployment_dirs:
            deployment_directory = os.path.join(base_directory, deployment_id)

            # Skip deployment IDs as defined in config
            if deployment_id in config['exclude_deployments']:
                continue

            # Assign window size based on specific deployment IDs
            window_size = config['custom_window_size'].get(deployment_id, config['default_window_size'])

            pbar.update(1)
            pbar.set_postfix({'current deployment': str(deployment_id)})

            if os.path.isdir(deployment_directory):
                process_deployment(deployment_directory, deployment_id, window_size, pbar)

    pbar.close()


# Process each deployment
def process_deployment(deployment_directory, deployment_id, window_size, pbar):
    list_filenames = os.listdir(deployment_directory)
    with tqdm(total=len(list_filenames), desc="{} [PROCESSING] {}".format(time.strftime("%H:%M:%S"), deployment_id),
              position=0, leave=True) as pbar_files:
        for file_iter, filename in enumerate(list_filenames):
            if filename.endswith('.csv'):
                process_csv_file(filename, deployment_directory, deployment_id, window_size, file_iter, pbar_files)


# Process each CSV file within a deployment

def process_csv_file(filename, deployment_directory, deployment_id, window_size, file_iter, pbar_files):
    pbar_files.set_description(
        "{} [PROCESSING] Calculating distance for {}".format(time.strftime("%H:%M:%S"), str(filename)))
    pbar_files.update(1)
    filename = os.path.join(deployment_directory, filename)

    start_timestamp, end_timestamp, station, start_lon, start_lat = process_deployment_data(base_directory,
                                                                                            dict_id_to_station,
                                                                                            filename)

    df = process_data(filename, start_lat, start_lon, csv_location, station, deployment_id, file_iter)
    df_smoothed = df.copy()
    pbar_files.set_description(
        "{} [PROCESSING] Finding closest ships".format(time.strftime("%H:%M:%S")))
    df_smoothed= create_closest_ships(df_smoothed, window_size)

    min_day, max_day = calculate_date_range(df, deployment_id)
    min_day=min_day #+ timedelta(days=1)
    day_start = 1
    days_between = (max_day - min_day).days
    next_day = min_day + timedelta(days=1)
    pbar_files.set_description(
        "{} [PROCESSING] Looping over days for deployment {} in station {}".format(time.strftime("%H:%M:%S"),deployment_id,station))
    while (max_day - next_day) >= timedelta(hours=1):
        pbar_files.set_postfix({
            "Last updated time": f"{time.strftime('%H:%M:%S')}",
            "day": f"{day_start} of {days_between}"
        })

        df_filtered = filter_dataframe_by_date(df, min_day, next_day)
        loc = determine_data_location(station, min_day)

        df_smoothed_filtered_all = filter_smoothed_data(df_smoothed, min_day, next_day)
        df_smoothed_filtered = filter_date(df_smoothed_filtered_all, hourly_intervals_date, deployment_id)
        if len(df_filtered) < 10 or len(df_smoothed_filtered) < 10:
            pbar_files.set_postfix({'comment': f"skipping {day_start} due to insufficient data"})
            day_start += 1
            min_day += timedelta(days=1)
            next_day += timedelta(days=1)
            continue

        df_samples, data = process_data_samples(df_smoothed_filtered, station, deployment_id, data_per_station, loc,raw_data_folder)
        if data.empty:
            pbar_files.set_postfix({'comment': f"skipping {day_start} due wrong day"})
            day_start += 1
            min_day += timedelta(days=1)
            next_day += timedelta(days=1)
            continue
        desired_filename = min_day.strftime("%y%m%d.nc")
        # print(min_day,desired_filename)


        database_creater(station, data, deployment_id,  df_samples,csv_file_database )

        day_start += 1
        min_day += timedelta(days=1)
        next_day += timedelta(days=1)

    pbar_files.set_postfix({})
    pbar_files.set_description("{} [FINISHED] Deployment {}".format(time.strftime("%H:%M:%S"), str(deployment_id)))



if __name__ == "__main__":
    main()
