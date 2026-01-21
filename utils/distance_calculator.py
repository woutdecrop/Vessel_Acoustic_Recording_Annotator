import os
import pandas as pd
import math
import time
# Function to calculate Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    radius = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

# Function to create and save distance vs. time plot

def process_latitude_column(df, column_name):
    try:
        df[column_name] = pd.to_numeric(df[column_name])
        return df
    except ValueError:
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

        # Count and print the number of rows with NaN in the column
        nan_count = df[column_name].isna().sum()
        # print(f"Number of rows with NaN in '{column_name}': {nan_count}")

        # Remove rows with NaN values in the column
        df.dropna(subset=[column_name], inplace=True)
        return df


def process_data(filename, start_lat, start_lon, csv_location, station, deployment_id, file_iter,range=20):
    filename_saved = os.path.join(csv_location,
                                  f'{deployment_id}_{station}-{start_lat}_{start_lon}_{file_iter}.csv')
    try:
        print("{} [PROCESSING] Load pre-processed file".format(time.strftime("%H:%M:%S")))
        df = pd.read_csv(filename_saved, low_memory=False)
        df["event_time"] = pd.to_datetime(df["event_time"])
        # print("already exists")
        valid_types = {'Tanker', 'Towing', 'Diving', 'Sailing', 'Passenger', 'Fishing', 'Tug', 'Other', 'Large Towing',
                       'Dredging', 'S&R', 'Pleasure Craft', 'High Speed Craft', 'Cargo',
                       'Pilot', 'Reserved', 'Anti-pollution equipment'}

        # Function to replace invalid types
        df['type'] = df['type'].apply(lambda x: x if x in valid_types else 'Other')

    except:
        print("{} [PROCESSING] processing distance".format(time.strftime("%H:%M:%S")))
        selected_columns = ["mmsi", "longitude", "latitude", "event_time", "type", "msg_type_description",
                            "sog"]
        df = pd.read_csv(filename, usecols=selected_columns, low_memory=False)

        start_lat = float(start_lat)
        start_lon = float(start_lon)
        # Convert 'latitude' column to numeric with 'coerce' option
        df = process_latitude_column(df, 'latitude')
        df = process_latitude_column(df, 'longitude')
        df['distance'] = df.apply(
            lambda row: haversine_distance(start_lat, start_lon, row['latitude'], row['longitude']), axis=1)
        # df_short = df.iloc[0:5]
        # df_short['distance'] = df_short.apply(lambda row: haversine_distance(start_lat, start_lon, row['latitude'], row['longitude']),
        #                           axis=1)
        if range!=100:
            df = df[df["distance"] < range]
        try:
            df["event_time"] = pd.to_datetime(df["event_time"])
        except:
            df["event_time"] = pd.to_datetime(df["event_time"], format='ISO8601', errors='coerce')

        df = df[
            ["mmsi", "longitude", "latitude", "event_time", "type", "distance", "msg_type_description", "sog"]]

        df.to_csv(filename_saved, index=False)

    return df

def process_data_excels(filename, start_lat, start_lon, csv_location, station, deployment_id, file_iter,range=20):
    filename_saved = os.path.join(csv_location,
                                  f'{deployment_id}_{station}-{start_lat}_{start_lon}_{file_iter}.csv')
    filename_saved_share = os.path.join(csv_location,
                                  f'{deployment_id}_{station}-{start_lat}_{start_lon}_{file_iter}_SHARE.csv')

    if os.path.exists(filename_saved_share):
        return
    else:
        print("{} [PROCESSING] processing distance".format(time.strftime("%H:%M:%S")))
        selected_columns = ["mmsi", "longitude", "latitude", "event_time", "type", "msg_type_description",
                            "sog"]
        df = pd.read_csv(filename, usecols=selected_columns, low_memory=False)

        start_lat = float(start_lat)
        start_lon = float(start_lon)
        # Convert 'latitude' column to numeric with 'coerce' option
        df = process_latitude_column(df, 'latitude')
        df = process_latitude_column(df, 'longitude')
        df['distance'] = df.apply(
            lambda row: haversine_distance(start_lat, start_lon, row['latitude'], row['longitude']), axis=1)
        # df_short = df.iloc[0:5]
        # df_short['distance'] = df_short.apply(lambda row: haversine_distance(start_lat, start_lon, row['latitude'], row['longitude']),
        #                           axis=1)
        df["distance"] = df["distance"].round(3)

        if range!=100:
            df = df[df["distance"] < range]
        try:
            df["event_time"] = pd.to_datetime(df["event_time"])
        except:
            df["event_time"] = pd.to_datetime(df["event_time"], format='ISO8601', errors='coerce')

        df = df[
            ["mmsi", "longitude", "latitude", "event_time", "type", "distance", "msg_type_description", "sog"]]

        df.to_csv(filename_saved, index=False)


        # Rename MMSI values to ship_number and remove original MMSI
        if 'mmsi' in df.columns:
            unique_mmsi = df['mmsi'].unique()
            mmsi_map = {mmsi: f"ship_{i + 1:03d}" for i, mmsi in enumerate(unique_mmsi)}
            df['ship_number'] = df['mmsi'].map(mmsi_map)
            df_privacy = df.drop(columns=['mmsi'])


        df_privacy.to_csv(filename_saved_share, index=False)

    return df



def categorize_distance(distance):
    if distance == '10+':
        return 10
    else:
        distance_split = distance.split('-')
        if len(distance_split) == 2:
            lower_bound = int(distance_split[0])
            upper_bound = int(distance_split[1])
            # Calculate the midpoint of the range
            distance_num = (lower_bound + upper_bound) / 2
            return distance_num
        else:
            return -1  # Handle invalid distances