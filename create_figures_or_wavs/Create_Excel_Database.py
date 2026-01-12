import os
import random
import sys
import time
from datetime import timedelta
from tqdm import tqdm

sys.path.append(r'/')
# from utils import (
#     dict_id_to_station,
#     hourly_intervals_date,
# )

from utils.audio_vessel_annotator import process_deployment_data
from utils.distance_calculator import process_data_excels



from utils.import_data import (
    dict_id_to_station,
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

    process_data_excels(filename, start_lat, start_lon, csv_location, station, deployment_id, file_iter,range=100)

if __name__ == "__main__":
    main()
