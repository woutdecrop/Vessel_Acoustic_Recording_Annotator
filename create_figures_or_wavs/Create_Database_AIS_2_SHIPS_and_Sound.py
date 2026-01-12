import os
import random
import sys
import csv
import time
from datetime import timedelta
from tqdm import tqdm

sys.path.append(r'/')


from utils import (
    dict_id_to_station,
    hourly_intervals_date,
)

from utils.audio_vessel_annotator import process_deployment_data, filter_date
from utils.distance_calculator import process_data
from utils.find_closest_wav import create_closest_ships_two, create_data
from utils.plot_spectrogram_distance import database_creater_two
from utils.data_processing_utils import (
    calculate_date_range,
    filter_dataframe_by_date,
    determine_data_location,
    filter_smoothed_data,
    process_data_samples_two,
)


from utils.import_data import (
    desired_pairs_val,
    desired_pairs_test,
    dict_id_to_valid_time,
    dict_id_to_station,
    hourly_intervals_date,
)


# Constants and Configuration
base_directory = r'excel_AIS\raw_excel_AIS'
csv_location = r'excel_AIS\cmmi_data_all'
search_directory= r'hybrid_millidecade_bands'
window = 6
round_it = False
comment = f"subset_cmmi"
plot_location_two = rf'plots_per_station_{window}_{comment}'
data_per_station = rf'data\data_per_station_{window}_{comment}'
os.makedirs(plot_location_two, exist_ok=True)
os.makedirs(data_per_station, exist_ok=True)
random.seed(42)  # Set a specific seed for reproducibility

csv_file_database = rf'UC6\database.csv'
# Define the headers
headers = [
    "file_location",
    "event_time",
    "distance_1",
    "distance_2",
    "vessel_type_1",
    "vessel_type_2",
    "activity_1",
    "activity_2",
    "SOG_1",
    "SOG_2",
    "ship_001",
    "ship_002",
    "station"
]

# Check if the file exists, if not, create it with headers
if not os.path.exists(csv_file_database):
    with open(csv_file_database, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Write the header row

def main():
    deployment_dirs = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    print("{} [START] Looping over deployments".format(time.strftime("%H:%M:%S")))

    with tqdm(total=len(deployment_dirs), desc="{} [PROCESSING] Deployments".format(time.strftime("%H:%M:%S")),
              position=0, leave=True) as pbar:
        # print("")
        for i, deployment_id in enumerate(deployment_dirs):
            deployment_directory = os.path.join(base_directory, deployment_id)

            # Adjust window based on deployment ID
            if deployment_id in ['29187', '28434']:
                window_size = 5
            else:
                window_size = 6

            pbar.update(1)
            pbar.set_postfix({'current deployment': str(deployment_id)})

            if os.path.isdir(deployment_directory):
                process_deployment(deployment_directory, deployment_id, window_size, pbar)

    pbar.close()

def process_deployment(deployment_directory, deployment_id, window_size, pbar):
    list_filenames = os.listdir(deployment_directory)
    with tqdm(total=len(list_filenames), desc="{} [PROCESSING] {}".format(time.strftime("%H:%M:%S"), deployment_id),
              position=0, leave=True) as pbar_files:
        for file_iter, filename in enumerate(list_filenames):
            if filename.endswith('.csv'):
                process_csv_file(filename, deployment_directory, deployment_id, window_size, file_iter, pbar_files)

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
    df_smoothed= create_closest_ships_two(df_smoothed, window_size)

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

        # print(f"{time.strftime('%H:%M:%S')} [PROCESSING] Plotting for {str(min_day.date())} in {station} for deployment {deployment_id}")
        df_smoothed_filtered_all = filter_smoothed_data(df_smoothed, min_day, next_day)
        df_smoothed_filtered = filter_date(df_smoothed_filtered_all, hourly_intervals_date, deployment_id)
        if len(df_filtered) < 10 or len(df_smoothed_filtered) < 10:
            pbar_files.set_postfix({'comment': f"skipping {day_start} due to insufficient data"})
            day_start += 1
            min_day += timedelta(days=1)
            next_day += timedelta(days=1)
            continue

        df_samples, data = process_data_samples_two(df_smoothed_filtered, station, deployment_id, data_per_station, loc)
        if data.empty:
            pbar_files.set_postfix({'comment': f"skipping {day_start} due wrong day"})
            day_start += 1
            min_day += timedelta(days=1)
            next_day += timedelta(days=1)
            continue
        desired_filename = min_day.strftime("%y%m%d.nc")
        # print(min_day,desired_filename)
        database_creater_two(station, min_day, data, deployment_id, df_filtered, df_smoothed_filtered, df_samples,
                      plot_location_two, search_directory, desired_filename, day_start, next_day,csv_file_database )

        day_start += 1
        min_day += timedelta(days=1)
        next_day += timedelta(days=1)

    pbar_files.set_postfix({})
    pbar_files.set_description("{} [FINISHED] Deployment {}".format(time.strftime("%H:%M:%S"), str(deployment_id)))

if __name__ == "__main__":
    main()
