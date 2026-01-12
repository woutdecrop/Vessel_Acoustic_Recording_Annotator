import os
import pandas as pd



def get_deployment_info(base_directory, filename):
    filename_parts = filename.split('_')
    start_lon = filename_parts[-4]
    start_lat = filename_parts[-3]

    filename = os.path.join(base_directory, filename)
    directory_path = os.path.dirname(filename)
    deployment_id = os.path.basename(directory_path)

    return filename_parts, start_lon, start_lat, filename, deployment_id


# Define a function to find and open the Xarray dataset


# Define a function to process a deployment
def process_deployment_data(base_directory, dict_id_to_station, filename):
    filename_parts, start_lon, start_lat, filename, deployment_id = get_deployment_info(base_directory, filename)

    station = dict_id_to_station.get(deployment_id)

    start_timestamp = pd.Timestamp(filename_parts[-2])
    end_timestamp = pd.Timestamp(filename_parts[-1][:-4])

    return start_timestamp,end_timestamp , station, start_lon, start_lat



def filter_date(df_smoothed_filtered,hourly_intervals_date ,deployment_id):

    hourly_intervals=hourly_intervals_date.get(deployment_id)
    filtered_df_date = df_smoothed_filtered #pd.DataFrame()
    start_len=len(filtered_df_date)
    for start_hour, end_hour in hourly_intervals:
        # start_hour=start_hour-pd.Timedelta(days=1)
        # end_hour = end_hour - pd.Timedelta(days=1)
        start_hour=start_hour.tz_localize('UTC')
        end_hour=end_hour.tz_localize('UTC')
        # break
        if start_hour == end_hour:  # Single hour
            df_smoothed_filtered= df_smoothed_filtered[df_smoothed_filtered['event_time'].dt.date != start_hour.date()]
        else:  # Hourly range
            df_smoothed_filtered= df_smoothed_filtered[~df_smoothed_filtered['event_time'].between(start_hour, end_hour)]
        # if len(filtered_df_date)!=len(df_smoothed_filtered):
        #     print(start_hour.date(), " is shortened for deploy", str(deployment_id), ' now ', len(filtered_df_date), '/', start_len)
            # print(len(filtered_df_date))
            # return filtered_df_date
    return df_smoothed_filtered