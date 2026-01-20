import warnings
from numba import NumbaDeprecationWarning
import pypam
import csv
import pandas as pd
from datetime import timedelta
import xarray as xr
from pydub import AudioSegment
import pypam.plots
from utils.import_data import type_colors
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
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


# #
def create_and_save_distance_vs_time_plot(df, df_min, df_samples, start_timestamp, end_timestamp, station, type_colors,
                                          ax, predicted_day=None):
    unique_types = df['type'].unique()
    legend_entries = []

    if predicted_day is None:
        # If no predicted_day, color vessels by type
        filtered_type_colors = {t: color for t, color in type_colors.items() if t in unique_types}
        for t, color in filtered_type_colors.items():
            color_with_alpha = color[:-1] + (0.4,)  # Adding alpha (transparency) value
            legend_entries.append(
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_with_alpha, markersize=6, label=t))

        # Plot vessel data
        for mmsi in df['mmsi'].unique():
            mmsi_data = df[df['mmsi'] == mmsi]
            smoothed_df = mmsi_data.set_index('event_time')
            mmsi_type = mmsi_data['type'].iloc[0]
            color = filtered_type_colors.get(mmsi_type, 'black')
            ax.plot(smoothed_df.index, smoothed_df['distance'], color=color, alpha=0.4)
            ax.scatter(smoothed_df.index, smoothed_df['distance'], color=color, alpha=0.4, s=10)  # Smaller grey points

        # Plot minimum distances with black line and black dots
        x_values = []
        y_values = []

        for i in range(len(df_min) - 1):
            time_diff = (df_min['event_time'].iloc[i + 1] - df_min['event_time'].iloc[i]).total_seconds() / 60.0

            if time_diff <= 15:
                x_values.append(df_min['event_time'].iloc[i])
                y_values.append(df_min['distance'].iloc[i])
            else:
                if x_values:
                    x_values.append(df_min['event_time'].iloc[i])
                    y_values.append(df_min['distance'].iloc[i])
                    ax.plot(x_values, y_values, color='black', linewidth=2)
                    ax.scatter(x_values, y_values, color='black', alpha=0.8, s=20)  # Adding small black points
                    x_values = []
                    y_values = []

        if x_values:
            x_values.append(df_min['event_time'].iloc[-1])
            y_values.append(df_min['distance'].iloc[-1])
            ax.plot(x_values, y_values, color='black', linewidth=2)
            ax.scatter(x_values, y_values, color='black', alpha=0.8, s=20)  # Adding small black points

        # Scatter plot for data points
        ax.scatter(df_samples["event_time"], df_samples["distance"], color='black', alpha=1.0, s=30, marker='o',
                   label='data points')
        legend_entries.append(plt.Line2D([0], [0], marker='o', color='black', markersize=6, label='data points'))
        ax.set_title(f"Distance of Vessels from Hydrophone, Categorized by Vessel Type")
    else:
        # If predicted_day is not None, color vessels grey
        light_grey = (0.7, 0.7, 0.7, 0.4)  # Lighter grey with alpha
        filtered_type_colors = {t: light_grey for t in unique_types}  # Apply grey to all types
        legend_entries.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=light_grey, markersize=6,
                                         label='other vessels'))

        # Plot vessel data in grey
        for mmsi in df['mmsi'].unique():
            mmsi_data = df[df['mmsi'] == mmsi]
            smoothed_df = mmsi_data.set_index('event_time')
            mmsi_type = mmsi_data['type'].iloc[0]
            color = filtered_type_colors.get(mmsi_type, 'black')
            ax.plot(smoothed_df.index, smoothed_df['distance'], color=color, alpha=0.4)
            ax.scatter(smoothed_df.index, smoothed_df['distance'], color=color, alpha=0.4, s=10)  # Smaller grey points

        # Plot minimum distances with black line and black dots
        x_values = []
        y_values = []

        for i in range(len(df_min) - 1):
            time_diff = (df_min['event_time'].iloc[i + 1] - df_min['event_time'].iloc[i]).total_seconds() / 60.0

            if time_diff <= 15:
                x_values.append(df_min['event_time'].iloc[i])
                y_values.append(df_min['distance'].iloc[i])
            else:
                if x_values:
                    x_values.append(df_min['event_time'].iloc[i])
                    y_values.append(df_min['distance'].iloc[i])
                    ax.plot(x_values, y_values, color='black', linewidth=2)
                    ax.scatter(x_values, y_values, color='black', alpha=0.8, s=20)  # Adding small black points
                    x_values = []
                    y_values = []

        if x_values:
            x_values.append(df_min['event_time'].iloc[-1])
            y_values.append(df_min['distance'].iloc[-1])
            ax.plot(x_values, y_values, color='black', linewidth=2)
            ax.scatter(x_values, y_values, color='black', alpha=0.8, s=20)  # Adding small black points


        # Plot predicted distances with gap filtering
        x_values, y_values = [], []
        predicted_day = predicted_day.sort_values(by='timestamp')
        for i in range(len(predicted_day) - 1):
            time_diff = (predicted_day["timestamp"].iloc[i + 1] - predicted_day["timestamp"].iloc[i]).total_seconds() / 60.0
            x_values.append(predicted_day["timestamp"].iloc[i])
            y_values.append(predicted_day["distance_number"].iloc[i])

            if time_diff > 25:
                if x_values:
                    ax.plot(x_values, y_values, color='blue', linewidth=2, alpha=0.8)
                    ax.scatter(x_values, y_values, color='blue', alpha=0.8, s=20)
                    x_values, y_values = [], []

        if x_values:
            x_values.append(predicted_day["timestamp"].iloc[-1])
            y_values.append(predicted_day["distance_number"].iloc[-1])
            ax.plot(x_values, y_values, color='blue', linewidth=2, alpha=0.8)
            ax.scatter(x_values, y_values, color='blue', alpha=0.8, s=20)

        legend_entries.append(plt.Line2D([0], [0], marker='o', color='blue', markersize=6, label='predicted'))
        legend_entries.append(plt.Line2D([0], [0], marker='o', color='black', markersize=6, label='closest vessel'))


        # Add black line and points to legend
        # legend_entries.append(plt.Line2D([0], [0], marker='o', color='black', markersize=6, label='closest vessel'))
        ax.set_title('Distance of Closest Vessels from Hydrophone with Models Predictions')

    ax.set_ylim(0, 11)
    ax.set_xlim(start_timestamp, end_timestamp)
    ax.set_xlabel('Time [h]')
    ax.set_ylabel('Distance [Km]')

    # Add the legend with smaller font size
    ax.legend(handles=legend_entries, loc='upper left', bbox_to_anchor=(1.02, 1.0), fontsize='small')

    # Set the x-axis major locator to display every hour
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    # Custom formatter function to handle the 24-hour label
    def custom_time_formatter(x, pos):
        hours = mdates.num2date(x).hour
        if hours == 0 and pos > 0:  # Handling the transition from 23h to 24h
            return '24h'
        return f'{hours}h'

    # Apply the custom formatter to the x-axis
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(custom_time_formatter))

    # Rotate x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)
    # Set y-axis ticks to every 1 km (or adjust interval as needed)
    yticks = np.arange(0, 11, 1)
    ax.set_yticks(yticks)

def save_plot(plot_location, fig, station, start_timestamp, deployment_id, predicted_day):
    station_output_dir = os.path.join(plot_location, station + '_' + str(deployment_id))
    os.makedirs(station_output_dir, exist_ok=True)
    plot_filename = f'{station}_{start_timestamp.strftime("%Y-%m-%d")}.png'
    plot_filepath = os.path.join(station_output_dir, plot_filename)


    first_fig_size = (1507, 832)
    fig.set_size_inches(first_fig_size[0] / fig.dpi, first_fig_size[1] / fig.dpi, forward=True)

    fig.savefig(plot_filepath, bbox_inches='tight')
    plt.close(fig)

    # Adding a print line with a timestamp
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if predicted_day is not None and not predicted_day.empty:
        print(f"{current_time} | Saved figure from Station {station} from {start_timestamp} at {plot_filepath}",
              end='\r', flush=True)


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

def database_creater_two(
    station,
    min_day,
    data,
    deployment_id,
    df_filtered,
    df_smoothed_filtered,
    df_samples,
    plot_location_two,
    search_directory,
    desired_filename,
    day_start,
    next_day,
    csv_file_database,
    predicted_day=None
):

    # Step 1: Create anonymized ship ID mapping
    all_mmsis = pd.concat([df_samples["mmsi_1"], df_samples["mmsi_2"]])
    unique_mmsis = all_mmsis.unique()
    mmsi_to_ship = {mmsi: f"ship_{i:03d}" for i, mmsi in enumerate(unique_mmsis, start=1)}

    # Step 2: Use mapping in your loop
    for index, row in data.iterrows():
        closest_wav_file = row['closest_wav_file']
        output_prefix = row['output_prefix']
        output_postfix = row['output_postfix']
        start_delta = row['start_delta']
        vessels_information = row["vessel_information"]

        if predicted_day is None:
            output_file = trim_wav(closest_wav_file, output_prefix, output_postfix, start_delta, station, deployment_id,
                                   vessels_information)
            file_location = output_file.split("\\")[-1]

            vessel_type_1, activity_1, SOG_1, vessel_type_2, activity_2, SOG_2 = vessels_information.split("_")

            distance_1 = df_samples["distance_1"].iloc[index]
            distance_2 = df_samples["distance_2"].iloc[index]

            # Anonymized ship IDs
            raw_mmsi_1 = df_samples["mmsi_1"].iloc[index]
            raw_mmsi_2 = df_samples["mmsi_2"].iloc[index]
            ship_001 = mmsi_to_ship[raw_mmsi_1]
            ship_002 = mmsi_to_ship[raw_mmsi_2]

            event_time = df_samples["event_time"].iloc[index]

            print("added to csv")

            with open(csv_file_database, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    file_location,
                    event_time,
                    distance_1,
                    distance_2,
                    vessel_type_1,
                    vessel_type_2,
                    activity_1,
                    activity_2,
                    SOG_1,
                    SOG_2,
                    ship_001,
                    ship_002,
                    station
                ])


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

def plot_analysis(
    station,
    min_day,
    data,
    deployment_id,
    df_filtered,
    df_smoothed_filtered,
    df_samples,
    plot_location_two,
    search_directory,
    desired_filename,
    day_start,
    next_day,
    predicted_day=None
):
    print("start")
    try:
        ds, dir, subdirectory = find_and_open_xr_dataset(search_directory, desired_filename, station)
    except:
        day_start += 1
        min_day += pd.Timedelta(days=1)
        next_day += pd.Timedelta(days=1)
        print("return")
        return

    fig, axes = plt.subplots(nrows=2, sharex='all', figsize=(20, 10))

    # Adjust the spacing between subplots
    plt.subplots_adjust(hspace=0.01)

    # General Title for the Figure
    # fig.suptitle(f'Analysis for {station} on {min_day.strftime("%Y-%m-%d")}', fontsize=16)

    # Upper subplot (ax1) for Long Term Spectrogram
    ax1 = axes[0]
    try:
        pypam.plots.plot_2d(
            ds['millidecade_bands'], x='datetime', y='frequency_bins', ax=ax1,
            cbar_label='psd [db]', xlabel='', ylabel='Frequency [Hz]',
            title=f'Long Term Spectrogram for {station} on {min_day.strftime("%Y-%m-%d")} ', ylog=True, vmin=50, vmax=120
        )
        for index, row in data.iterrows():
            closest_wav_file = row['closest_wav_file']
            output_prefix = row['output_prefix']
            output_postfix = row['output_postfix']
            start_delta = row['start_delta']
            vessels_information = row["vessel_information"]
            if predicted_day is None:
                output_file=trim_wav(closest_wav_file, output_prefix, output_postfix, start_delta, station, deployment_id, vessels_information)

    except:
        day_start += 1
        min_day += pd.Timedelta(days=1)
        next_day += pd.Timedelta(days=1)
        plt.close()
        return

    ax1.set_ylim([10, 14000])

    # Lower subplot (ax2) for the Distance vs. Time plot
    ax2 = axes[1]

    # Define the position and size of the lower plot
    lower_plot_rect = [0.125, 0.15, 0.62, 0.3]
    ax2.set_position(lower_plot_rect)
    ax2.axis('on')

    # Create and save the Distance vs. Time plot
    # create_and_save_distance_vs_time_plot(df_filtered, df_smoothed_filtered, df_samples, min_day, next_day, station, type_colors, ax2)
    create_and_save_distance_vs_time_plot(df_filtered, df_smoothed_filtered, df_samples, min_day, next_day, station, type_colors, ax2, predicted_day)
    # Save the plot
    save_plot(plot_location_two, fig, station, min_day, deployment_id, predicted_day)

# print("plotted here: ", plot_location_two)