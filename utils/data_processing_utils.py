# data_processing_utils.py

import pandas as pd
from datetime import timedelta
from utils.import_data import desired_pairs_test, desired_pairs_val, dict_id_to_valid_time
from utils.find_closest_wav import create_data
def calculate_date_range(df, deployment_id):
    min_day = df["event_time"].min().replace(hour=0, minute=0, second=0, microsecond=0)
    max_day = df["event_time"].max() + timedelta(days=1)
    valid_until = dict_id_to_valid_time.get(deployment_id)
    max_day = min(pd.Timestamp(valid_until).tz_localize('UTC'), max_day)
    return min_day, max_day

def filter_dataframe_by_date(df, min_day, next_day):
    return df[(df['event_time'] >= min_day) & (df['event_time'] <= next_day)]

def determine_data_location(station, min_day):
    loc = "train"
    for st, date in desired_pairs_test:
        if st == station and min_day.strftime('%Y-%m-%d') == date:
            loc = "test"
    for st, date in desired_pairs_val:
        if st == station and min_day.strftime('%Y-%m-%d') == date:
            loc = "val"
    return loc

def filter_smoothed_data(df_smoothed, min_day, next_day):
    return df_smoothed[(df_smoothed['event_time'] >= min_day) & (df_smoothed['event_time'] < next_day)]





def process_data_samples(df_smoothed_filtered, station, deployment_id, data_per_station, loc,root_folder_path = r'data'):
    df_samples = pd.DataFrame()
    data = pd.DataFrame(columns=['closest_wav_file', 'output_prefix', 'output_postfix', 'start_delta',
                                 'vessels_information'])
    selected_data = df_smoothed_filtered

    for index, row in selected_data.iterrows():
        target_date = row['event_time'].tz_convert(None).to_pydatetime()
        distance = str(round(row['distance'] * 1000))
        df_samples = pd.concat([df_samples, row.to_frame().T], ignore_index=True)
        vessels_information = row["vessel_information"].replace(' ', '-')
        extra, data, next = create_data(target_date, station, deployment_id, data_per_station,
                                        data, 0, distance, vessels_information, loc,root_folder_path)
        if next == "break":
            break
        elif next == "continue":
            continue

    df_samples.reset_index(drop=True, inplace=True)
    return df_samples, data


