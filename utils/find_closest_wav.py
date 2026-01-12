import pandas as pd
import numpy as np
import os
import datetime


def create_closest_ships_two(df_smoothed, window):
    # Preprocess
    filtered_df = df_smoothed.dropna(subset=["type", "event_time", "distance"])
    filtered_df['vessel_information'] = (
        filtered_df['type'].astype(str) + '_' +
        filtered_df['msg_type_description'].astype(str) + '_' +
        filtered_df['sog'].astype(str)
    )

    filtered_df['event_time'] = pd.to_datetime(filtered_df['event_time'])
    filtered_df.set_index('event_time', inplace=True)

    window_size = str(window) + 'T'

    # Sort by distance and pick top 2 per window
    grouped = (
        filtered_df
        .sort_values(by='distance')
        .groupby(pd.Grouper(freq=window_size), group_keys=False)
        .head(2)
        .reset_index()
    )

    # Add a rank (1 or 2) within each time window
    grouped['rank'] = grouped.groupby(pd.Grouper(key='event_time', freq=window_size)).cumcount() + 1

    # Pivot to wide format
    pivoted = grouped.pivot_table(
        index=pd.Grouper(key='event_time', freq=window_size),
        columns='rank',
        values=['mmsi', 'distance', 'vessel_information'],
        aggfunc='first'
    )

    # Flatten multi-index columns
    pivoted.columns = [f"{col}_{rank}" for col, rank in pivoted.columns]
    pivoted = pivoted.reset_index()

    return pivoted



def create_closest_ships(df_smoothed,window):

    filtered_df= df_smoothed
    filtered_df = filtered_df.dropna(subset=["type"])# .rolling(window=window_size).min()
    filtered_df['vessel_information'] = filtered_df['type'].astype(str) + '_' + filtered_df[
        'msg_type_description'].astype(
        str) + '_' + \
                                        filtered_df['sog'].astype(str)

    #
    filtered_df.set_index('event_time', inplace=True)

    # Define the fixed time window (e.g., 1 minute)
    window_size = str(window)+ 'T'  # 'T' stands for minute, 'H' for hour, 'D' for day, etc.

    try:
        def custom_idxmin(group):
            if group.empty:
                # Handle case where group is empty (no valid values)
                return pd.NaT  # Return a default value (NaT) or handle it accordingly
            else:
                return group.idxmin()

        filtered_df= filtered_df[filtered_df.index.notna()]
        min_distance_index = filtered_df.groupby(pd.Grouper(freq=window_size))['distance'].transform(custom_idxmin)
        # print(min_distance_index)  # Print intermediate result
    except Exception as e:
        print("Error occurred:", e)
    # Select the rows corresponding to the minimum distance within each time window
    # Remove duplicates based on index
    resampled_min_distance = filtered_df.loc[min_distance_index].drop_duplicates()
    resampled_min_distance

    resampled_min_distance = resampled_min_distance.dropna(subset=["distance"])
    resampled_min_distance.drop(['type', 'msg_type_description', 'sog'], axis=1, inplace=True)

    return resampled_min_distance.reset_index()



def filter_subfolders(subfolders, target_date):
    def filter_condition(subfolder):
        subfolder_date = datetime.datetime.strptime(subfolder, '%y%m%d').date()
        target_date_day = target_date.date()
        return subfolder_date == target_date_day

    return list(filter(filter_condition, subfolders))


def filter_folders(path, target_date,station):
    folders = []
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if os.path.isdir(folder_path) and station.lower() in folder_name.lower():
            if folder_name[0]=="_":
                continue
            folder_date = datetime.datetime.strptime(folder_name.split('_')[1], '%Y%m%d')
            if folder_date < target_date:
                folders.append((folder_path, folder_date))
    return folders

def wav_file_to_datetime(wav_file):
    date_str, time_str = wav_file.split('_')[1:3]
    datetime_str = f"{date_str} {time_str.split('.')[0]}"
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H-%M-%S')

def select_closest_wav_file(wav_files, target_date):


    wav_files.sort(key=lambda x: abs(wav_file_to_datetime(x) - target_date))

    selected_wav_file = None

    for wav_file in wav_files:
        wav_datetime = wav_file_to_datetime(wav_file)
        if wav_datetime <= target_date:
            selected_wav_file = wav_file
            break

    return selected_wav_file


def find_closest_wav_file(target_date,station):
    # target_date=df_smoothed_filtered["event_time"].iloc[100]
    # target_date = target_date.tz_convert(None).to_pydatetime()
    root_folder_path = r'PhD_Clea'
    stations = filter_folders(root_folder_path, target_date,station)

    if not stations:
        return "station", 0

    stations.sort(key=lambda x: x[1], reverse=True)
    selected_station = stations[0][0]
    records_folder = os.path.join(selected_station, 'records')

    # if not os.path.exists(records_folder):
    #     return None, 0

    items = os.listdir(records_folder)
    subfolders = [item for item in items if os.path.isdir(os.path.join(records_folder, item))]

    matching_subfolders = filter_subfolders(subfolders, target_date)

    if not matching_subfolders:
        return "day", 0

    selected_subfolder = matching_subfolders[-1]
    selected_subfolder_path = os.path.join(records_folder, selected_subfolder)
    wav_files = [file for file in os.listdir(selected_subfolder_path) if file.endswith('.wav')]

    # if not wav_files:
    #     return None, 0

    selected_wav_file = select_closest_wav_file(wav_files, target_date)

    if selected_wav_file:
        selected_wav_file_path = os.path.join(selected_subfolder_path, selected_wav_file)
        time_difference = (target_date - wav_file_to_datetime(selected_wav_file)).total_seconds()
        return selected_wav_file_path, time_difference
    # print("break")
    return "not_present", 0



def create_data(target_date, station, deployment_id, data_per_station, data,looper,distance,vessels_information,loc):
    closest_wav_file, start_delta = find_closest_wav_file(target_date, station)

    if closest_wav_file == "day":
        # print("day", target_date)
        return looper, data, "break"

    if closest_wav_file == "station":
        # print(f"station not found: {station}")
        return looper, data, "break"

    if closest_wav_file == "not_present":
        # print(f"wav not found: {target_date}")
        return looper, data, "continue"

    looper += 1
    # print("something")

    output_prefix = os.path.join(data_per_station, station + '_' + str(deployment_id) + '_' + loc)

    os.makedirs(output_prefix, exist_ok=True)

    date_str = target_date.strftime('%Y-%m-%d-%H-%M-%S')


    output_postfix = f"{distance}"
    new_data = {
        'closest_wav_file': closest_wav_file,
        'output_prefix': output_prefix,
        'output_postfix': output_postfix,
        'start_delta': start_delta,
        'vessel_information': vessels_information
    }

    data = pd.concat([data, pd.DataFrame(new_data, index=[0])], ignore_index=True)

    return  looper, data, 'nothing'


