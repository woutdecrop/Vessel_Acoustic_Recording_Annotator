import warnings
from numba import NumbaDeprecationWarning
import csv
from datetime import timedelta
import xarray as xr
from pydub import AudioSegment
import datetime
import matplotlib.pyplot as plt
import os

plt.rcParams['text.usetex'] = False
warnings.filterwarnings("ignore", category=RuntimeWarning, module='pydub')
warnings.filterwarnings("ignore", category=NumbaDeprecationWarning, module='pypam')



def find_files(directory):
    subdirectories = []
    for root, dirs, files in os.walk(directory):
        subdirectories.append(files)
    return subdirectories

def find_subdirectories_with_name(directory, name):
    subdirectories = []
    for root, dirs, files in os.walk(directory):
        if name in root:
            # print(root)
            subdirectories.append(root)
    return subdirectories



def find_subdirectories_with_name(directory, name):
    subdirectories = []
    for root, dirs, files in os.walk(directory):
        if name in root:
            # print(root)
            subdirectories.append(root)
    return subdirectories

# Function to check if a specific file exists in a directory
def check_file_exists_in_directory(directory, filename):
    filename = os.path.join(directory, filename)
    return os.path.exists(filename)




def find_and_open_xr_dataset(search_directory, desired_filename, station):
    subdirectories = find_subdirectories_with_name(search_directory, station)

    if subdirectories:
        for subdirectory in subdirectories:
            # print(subdirectory)
            # print(os.path.join(subdirectory, desired_filename))
            if check_file_exists_in_directory(subdirectory, desired_filename):
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time} | File '{desired_filename}' found in '{subdirectory}'.", end='\r', flush=True)
                dir=str(os.path.basename(subdirectory))
                path = os.path.join(subdirectory, desired_filename)
                ds = xr.open_dataset(path)
                return ds,dir,subdirectory
    print("none")
    return None



def trim_wav(input_file, output_prefix,output_postfix,start_delta,station,deployment_id,vessels_information):
    snippet_duration = 10 #9.614  # Length of each snippet in seconds
    # audio[:9614]
    overlap_duration = 2   # Overlap duration in seconds

    # Read the WAV file
    # audio = AudioSegment.from_wav(input_file)

    ext = os.path.splitext(input_file)[1].lower()

    if ext == ".wav":
        audio = AudioSegment.from_wav(input_file)
    elif ext == ".flac":
        audio = AudioSegment.from_file(input_file, format="flac")
    else:
        raise ValueError(f"Unsupported audio format: {ext}")

    date_str, time_str = str(input_file).split("\\")[-1].split('_')[1:]
    datetime_str = date_str + '_' + time_str.split('.')[0]
    start_file= datetime.datetime.strptime(datetime_str, '%Y-%m-%d_%H-%M-%S')
    start_time = start_delta
    # Calculate the start and end positions in milliseconds
    start_pos = start_time * 1000
    end_pos = (start_time + snippet_duration) * 1000

    start_file=start_file+timedelta(seconds=start_time)
    end_file=start_file+timedelta(seconds=snippet_duration)
    # Check if the end_pos exceeds the total duration of the audio
    if end_pos > len(audio):
        end_pos = len(audio)

    # Extract the desired timeframe, trimmed_audio
    trimmed_audio = audio[start_pos:end_pos]

    # Return the duration of the trimmed audio in seconds
    duration_seconds = len(trimmed_audio) / 1000
    start_delta=str(start_delta).replace('.', '-')
    vessels_information=vessels_information.replace(".", "-")
    station_letter=station[0]


    output_file = f"{output_prefix}/{deployment_id}_{datetime_str}_{start_delta}_{vessels_information}_{output_postfix}.wav"
    trimmed_audio.export(output_file, format="wav")

    # Move the start_time forward with overlap_duration to create an overlap
    start_time += snippet_duration - overlap_duration


    return output_file


def database_creater(
    station,
    data,
    deployment_id,
    df_samples,
    csv_file_database,
    predicted_day=None
):
    print("start")

    for index, row in data.iterrows():
        closest_wav_file = row['closest_wav_file']
        output_prefix = row['output_prefix']
        output_postfix = row['output_postfix']
        start_delta = row['start_delta']
        vessels_information = row["vessel_information"]
        if predicted_day is None:
            output_file=trim_wav(closest_wav_file, output_prefix, output_postfix, start_delta, station, deployment_id, vessels_information)
            file_location=output_file.split("\\")[-1]
            vessel_type=row["vessel_information"].split("_")[0]
            activity=row["vessel_information"].split("_")[1]
            SOG = row["vessel_information"].split("_")[2]
            mmsi=df_samples["mmsi"].iloc[index]
            longitude = df_samples["longitude"].iloc[index]
            latitude = df_samples["latitude"].iloc[index]
            distance= df_samples["distance"].iloc[index]
            event_time=df_samples["event_time"].iloc[index]
            # print("added to csv")
            # Append data to CSV
            with open(csv_file_database, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([file_location, vessel_type, activity, SOG, mmsi, longitude, latitude, distance, event_time,station])
