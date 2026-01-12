import pandas as pd
import random
random.seed(42)  # Set a specific seed for reproducibility
dict_id_to_station = {'15810': 'Grafton', '28434': 'Grafton', '25712': 'Faulbaums', '26982': 'Belwind',
                      '29187': 'Grafton','15811':'GardenCity','15812':'Buitenratel','26981':'GardenCity'}

dict_id_to_valid_time = {'15810': '2022-05-11', '28434': '2022-10-27', '25712': '2022-06-19', '26982': '2022-07-22',
                      '29187': '2022-11-08','15811': '2022-05-23','15812':'2022-05-16','26981':'2022-07-01'}
hourly_intervals_28434 = [
    (pd.to_datetime('2022-08-20 04:00:00'), pd.to_datetime('2022-08-22 04:30:00')),
    (pd.to_datetime('2022-08-22 03:00:00'), pd.to_datetime('2022-08-22 14:00:00')),
    (pd.to_datetime('2022-08-22 18:00:00'), pd.to_datetime('2022-08-22 21:00:00')),
    (pd.to_datetime('2022-08-24 07:40:00'), pd.to_datetime('2022-08-24 07:55:00')),
    (pd.to_datetime('2022-08-28 23:25:00'), pd.to_datetime('2022-08-29 00:00:00')),
    (pd.to_datetime('2022-09-03 08:45:00'), pd.to_datetime('2022-09-03 09:00:00')),
    (pd.to_datetime('2022-09-05 06:00:00'), pd.to_datetime('2022-09-05 20:00:00')),
    # Add more hourly intervals or single hours as needed
]

hourly_intervals_29187 = [
    (pd.to_datetime('2022-10-28 06:00:00'), pd.to_datetime('2022-10-28 13:00:00')),
    # Add more hourly intervals or single hours as needed
]

# (pd.to_datetime('2022-01-24 08:50:00'), pd.to_datetime('2022-01-24 09:10:00')),
# (pd.to_datetime('2022-01-24 15:00:00'), pd.to_datetime('2022-01-24 15:30:00')),

hourly_intervals_15811 = [
    (pd.to_datetime('2022-01-20 08:00:00'), pd.to_datetime('2022-01-20 08:30:00')),
    (pd.to_datetime('2022-01-20 19:30:00'), pd.to_datetime('2022-01-20 20:00:00')),
    (pd.to_datetime('2022-01-24 08:50:00'), pd.to_datetime('2022-01-24 09:10:00')),
    (pd.to_datetime('2022-01-24 15:00:00'), pd.to_datetime('2022-01-24 15:30:00')),
    # (pd.to_datetime('2022-01-26 11:45:00'), pd.to_datetime('2022-01-26 12:05:00')),
    (pd.to_datetime('2022-01-28 07:00:00'), pd.to_datetime('2022-01-28 07:30:00')),
    (pd.to_datetime('2022-01-28 20:30:00'), pd.to_datetime('2022-01-28 22:15:00')),
    # (pd.to_datetime('2022-01-28 23:00:00'), pd.to_datetime('2022-01-28 23:30:00')),
    # (pd.to_datetime('2022-01-30 05:00:00'), pd.to_datetime('2022-01-30 05:30:00')),
    (pd.to_datetime('2022-01-30 17:00:00'), pd.to_datetime('2022-01-30 18:30:00')),
    (pd.to_datetime('2022-01-30 19:45:00'), pd.to_datetime('2022-01-30 20:00:00')),
    (pd.to_datetime('2022-01-30 20:45:00'), pd.to_datetime('2022-01-30 21:00:00')),
    (pd.to_datetime('2022-02-01 01:00:00'), pd.to_datetime('2022-02-01 04:30:00')),
    (pd.to_datetime('2022-02-01 20:00:00'), pd.to_datetime('2022-02-01 22:30:00')),
    (pd.to_datetime('2022-02-03 02:30:00'), pd.to_datetime('2022-02-04 03:00:00')),
    (pd.to_datetime('2022-02-03 06:30:00'), pd.to_datetime('2022-02-04 07:00:00')),
    (pd.to_datetime('2022-02-03 19:30:00'), pd.to_datetime('2022-02-04 00:00:00')),
    (pd.to_datetime('2022-02-03 19:30:00'), pd.to_datetime('2022-02-04 00:00:00')),
    (pd.to_datetime('2022-02-05 05:30:00'), pd.to_datetime('2022-02-05 08:30:00')),
    (pd.to_datetime('2022-02-05 18:00:00'), pd.to_datetime('2022-02-05 18:30:00')),
    (pd.to_datetime('2022-02-07 01:00:00'), pd.to_datetime('2022-02-07 01:30:00')),
    (pd.to_datetime('2022-02-07 07:30:00'), pd.to_datetime('2022-02-07 07:50:00')),
    (pd.to_datetime('2022-02-07 18:00:00'), pd.to_datetime('2022-02-07 18:15:00')),
    # (pd.to_datetime('2022-02-09 15:00:00'), pd.to_datetime('2022-02-09 17:00:00')),
    (pd.to_datetime('2022-02-11 04:00:00'), pd.to_datetime('2022-02-11 05:00:00')),
    (pd.to_datetime('2022-02-11 14:10:00'), pd.to_datetime('2022-02-11 15:00:00')),
    (pd.to_datetime('2022-02-13 23:00:00'), pd.to_datetime('2022-02-13 23:30:00')),
    (pd.to_datetime('2022-02-15 00:45:00'), pd.to_datetime('2022-02-15 01:30:00')),
    (pd.to_datetime('2022-02-15 11:30:00'), pd.to_datetime('2022-02-15 18:00:00')),
    (pd.to_datetime('2022-02-17 00:00:00'), pd.to_datetime('2022-02-17 06:00:00')),
    (pd.to_datetime('2022-02-17 13:30:00'), pd.to_datetime('2022-02-17 14:30:00')),
    (pd.to_datetime('2022-02-19 10:00:00'), pd.to_datetime('2022-02-19 11:30:00')),
    (pd.to_datetime('2022-02-19 14:30:00'), pd.to_datetime('2022-02-19 16:55:00')),
    (pd.to_datetime('2022-02-19 20:00:00'), pd.to_datetime('2022-02-19 20:10:00')),
    (pd.to_datetime('2022-02-19 23:30:00'), pd.to_datetime('2022-02-20 00:00:00')),
    (pd.to_datetime('2022-02-21 08:15:00'), pd.to_datetime('2022-02-21 08:45:00')),
    (pd.to_datetime('2022-02-21 11:00:00'), pd.to_datetime('2022-02-21 16:00:00')),
    (pd.to_datetime('2022-02-21 18:00:00'), pd.to_datetime('2022-02-21 19:30:00')),
    (pd.to_datetime('2022-02-21 06:00:00'), pd.to_datetime('2022-02-21 06:15:00')),
    (pd.to_datetime('2022-02-23 09:00:00'), pd.to_datetime('2022-02-23 12:00:00')),
    (pd.to_datetime('2022-02-23 14:00:00'), pd.to_datetime('2022-02-23 14:20:00')),
    (pd.to_datetime('2022-02-23 18:50:00'), pd.to_datetime('2022-02-23 20:00:00')),
    (pd.to_datetime('2022-02-25 10:30:00'), pd.to_datetime('2022-02-25 10:50:00')),
    (pd.to_datetime('2022-02-27 07:00:00'), pd.to_datetime('2022-02-27 07:10:00')),
    (pd.to_datetime('2022-02-27 10:00:00'), pd.to_datetime('2022-02-27 11:00:00')),
    (pd.to_datetime('2022-03-01 20:00:00'), pd.to_datetime('2022-03-01 20:30:00')),
    (pd.to_datetime('2022-03-01 10:30:00'), pd.to_datetime('2022-03-01 11:00:00')),
    # (pd.to_datetime('2022-03-03 16:30:00'), pd.to_datetime('2022-03-03 17:30:00')),
    (pd.to_datetime('2022-03-07 09:00:00'), pd.to_datetime('2022-03-07 15:00:00')),
    (pd.to_datetime('2022-03-09 06:00:00'), pd.to_datetime('2022-03-09 11:00:00')),
    (pd.to_datetime('2022-03-17 00:00:00'), pd.to_datetime('2022-03-17 03:00:00')),
    (pd.to_datetime('2022-03-17 17:00:00'), pd.to_datetime('2022-03-17 19:30:00')),
    (pd.to_datetime('2022-03-21 03:45:00'), pd.to_datetime('2022-03-21 06:00:00')),
    (pd.to_datetime('2022-03-29 02:20:00'), pd.to_datetime('2022-03-29 02:40:00')),
    (pd.to_datetime('2022-03-29 05:00:00'), pd.to_datetime('2022-03-29 06:30:00')),
    (pd.to_datetime('2022-03-29 10:00:00'), pd.to_datetime('2022-03-29 11:00:00')),
    (pd.to_datetime('2022-04-06 15:40:00'), pd.to_datetime('2022-04-06 16:30:00')),
    (pd.to_datetime('2022-04-22 09:55:00'), pd.to_datetime('2022-04-22 10:05:00')),
    (pd.to_datetime('2022-04-28 15:30:00'), pd.to_datetime('2022-04-28 17:00:00')),
    (pd.to_datetime('2022-04-30 09:30:00'), pd.to_datetime('2022-04-30 10:00:00')),
    (pd.to_datetime('2022-05-02 11:10:00'), pd.to_datetime('2022-05-02 12:00:00')),
    (pd.to_datetime('2022-05-02 22:30:00'), pd.to_datetime('2022-05-02 22:40:00')),
    (pd.to_datetime('2022-05-04 08:00:00'), pd.to_datetime('2022-05-04 09:00:00')),
    (pd.to_datetime('2022-05-10 23:40:00'), pd.to_datetime('2022-05-11 00:00:00')),
    (pd.to_datetime('2022-05-12 15:45:00'), pd.to_datetime('2022-05-10 16:00:00')),
    (pd.to_datetime('2022-05-16 04:00:00'), pd.to_datetime('2022-05-16 05:00:00')),
    (pd.to_datetime('2022-05-16 11:50:00'), pd.to_datetime('2022-05-16 12:15:00')),
    (pd.to_datetime('2022-05-16 19:40:00'), pd.to_datetime('2022-05-16 20:15:00')),
    (pd.to_datetime('2022-05-18 06:00:00'), pd.to_datetime('2022-05-17 14:05:00')),
    # (pd.to_datetime('2022-05-18 06:00:00'), pd.to_datetime('2022-05-18 16:15:00')),
    (pd.to_datetime('2022-05-18 20:00:00'), pd.to_datetime('2022-05-18 21:00:00')),
    (pd.to_datetime('2022-05-20 13:00:00'), pd.to_datetime('2022-05-20 13:15:00')),
]
# hourly_intervals_15811=[]

hourly_intervals_15810 = [
    (pd.to_datetime('2022-01-20 15:10:00'), pd.to_datetime('2022-01-20 16:15:00')),  # Adding a missing entry
    (pd.to_datetime('2022-01-28 06:00:00'), pd.to_datetime('2022-01-28 21:00:00')),
    (pd.to_datetime('2022-02-13 17:00:00'), pd.to_datetime('2022-02-13 17:30:00')),
    (pd.to_datetime('2022-02-15 17:00:00'), pd.to_datetime('2022-02-16 00:00:00')),
    (pd.to_datetime('2022-02-15 12:30:00'), pd.to_datetime('2022-02-15 12:45:00')),
    (pd.to_datetime('2022-02-15 09:30:00'), pd.to_datetime('2022-02-15 10:45:00')),
    # (pd.to_datetime('2022-02-19 00:00:00'), pd.to_datetime('2022-02-19 20:00:00')),
    (pd.to_datetime('2022-02-21 05:50:00'), pd.to_datetime('2022-02-21 06:00:00')),
    (pd.to_datetime('2022-02-21 15:30:00'), pd.to_datetime('2022-02-21 16:00:00')),
    (pd.to_datetime('2022-02-23 22:10:00'), pd.to_datetime('2022-02-23 23:00:00')),
    (pd.to_datetime('2022-03-03 06:00:00'), pd.to_datetime('2022-03-03 12:00:00')),
    (pd.to_datetime('2022-03-05 01:10:00'), pd.to_datetime('2022-03-05 01:50:00')),
    # (pd.to_datetime('2022-03-09 12:00:00'), pd.to_datetime('2022-03-09 14:30:00')),
    (pd.to_datetime('2022-03-11 18:30:00'), pd.to_datetime('2022-03-11 19:30:00')),
    (pd.to_datetime('2022-03-11 11:30:00'), pd.to_datetime('2022-03-11 14:00:00')),
    (pd.to_datetime('2022-03-13 08:30:00'), pd.to_datetime('2022-03-13 08:45:00')),
    (pd.to_datetime('2022-03-17 06:00:00'), pd.to_datetime('2022-03-17 06:00:00')),
    (pd.to_datetime('2022-03-19 03:30:00'), pd.to_datetime('2022-03-19 04:10:00')),
    (pd.to_datetime('2022-03-21 21:30:00'), pd.to_datetime('2022-03-21 22:00:00')),
    (pd.to_datetime('2022-03-23 08:00:00'), pd.to_datetime('2022-03-23 08:30:00')),
    (pd.to_datetime('2022-03-29 06:00:00'), pd.to_datetime('2022-03-29 08:00:00')),
    (pd.to_datetime('2022-03-31 16:00:00'), pd.to_datetime('2022-03-31 23:59:00')),
    (pd.to_datetime('2022-03-29 07:00:00'), pd.to_datetime('2022-03-29 08:00:00')),
    (pd.to_datetime('2022-04-08 10:00:00'), pd.to_datetime('2022-04-08 11:00:00')),
    (pd.to_datetime('2022-04-08 23:00:00'), pd.to_datetime('2022-04-08 23:59:00')),
    (pd.to_datetime('2022-04-12 01:20:00'), pd.to_datetime('2022-04-12 01:40:00')),
    (pd.to_datetime('2022-04-28 15:00:00'), pd.to_datetime('2022-04-29 00:00:00')),
    (pd.to_datetime('2022-04-30 10:00:00'), pd.to_datetime('2022-04-30 11:00:00')),
    (pd.to_datetime('2022-05-02 12:15:00'), pd.to_datetime('2022-05-02 13:00:00')),
    (pd.to_datetime('2022-05-04 06:00:00'), pd.to_datetime('2022-05-04 17:00:00')),
]
# hourly_intervals_15810=[]
hourly_intervals_26981 = [
    (pd.to_datetime('2022-06-24 15:15:00'), pd.to_datetime('2022-06-24 16:00:00')),
    (pd.to_datetime('2022-06-26 00:00:00'), pd.to_datetime('2022-06-26 00:30:00')),
    (pd.to_datetime('2022-06-26 02:15:00'), pd.to_datetime('2022-06-26 02:45:00')),
    (pd.to_datetime('2022-06-26 19:45:00'), pd.to_datetime('2022-06-26 20:10:00')),
    (pd.to_datetime('2022-06-28 00:00:00'), pd.to_datetime('2022-06-28 00:00:00')),
    (pd.to_datetime('2022-06-29 00:00:00'), pd.to_datetime('2022-06-29 00:00:00')),  # Single hour
]
# hourly_intervals_26981=[]

hourly_intervals_date = {'15810': hourly_intervals_15810, '28434': hourly_intervals_28434, '25712': hourly_intervals_15810, '26982': hourly_intervals_15810,
                      '29187': hourly_intervals_29187,'15811': hourly_intervals_15811,'15812':hourly_intervals_15810,'26981':hourly_intervals_26981}

import matplotlib.cm as cm
colormap = cm.get_cmap('tab10')
colormap = cm.get_cmap('tab10', 10)

# Define the color scheme
type_colors = {
    # Most frequent types with the requested colors
    'Tanker': colormap(1),  # Orange
    'Pilot': colormap(0),  # Blue
    'Cargo': (0.529, 0.737, 0.898, 1.0), # Light Blue (manual value, close to light blue)
    'Fishing': colormap(2),  # Green
    'Tug': colormap(3),  # Light Orange (from tab10, approximated)
    'Passenger': colormap(4),  # Light Green (from tab10, approximated)

    # Less common types with varied colors not resembling green, blue, or orange
    'High Speed Craft': colormap(5),  # Red
    'Dredging': colormap(6),  # Purple
    'Other': colormap(7),  # Gray
    'Military': colormap(8),  # Brown
    'Reserved': colormap(9),  # Light Brown/Beige
    'Sailing': (0.7372549019607844, 0.7411764705882353, 0.13333333333333333, 1.0),  # Olive
    'Diving': (0.09019607843137255, 0.7450980392156863, 0.8117647058823529, 1.0),  # Turquoise
    'S&R': (0.4980392156862745, 0.4980392156862745, 0.4980392156862745, 1.0),  # Gray
    'Towing': (0.7803921568627451, 0.7803921568627451, 0.7803921568627451, 1.0),  # Light Gray
    'Law Enforcement': (0.8588235294117647, 0.8588235294117647, 0.5529411764705883, 1.0),  # Light Yellow
    'Pleasure Craft': (0.6196078431372549, 0.8549019607843137, 0.8980392156862745, 1.0),  # Light Cyan
    'Anti-pollution equipment': (0.9686274509803922, 0.7137254901960784, 0.8235294117647058, 1.0),  # Light Pink
    'Large Towing': (0.8901960784313725, 0.4666666666666667, 0.7607843137254902, 1.0)  # Pink
}



grafton_dates = [
    "2022-01-22",
    "2022-02-07",
    "2022-02-03",
    '2022-02-11',
    "2022-02-23",
    "2022-03-15",
    "2022-04-18",
    "2022-08-28",
    "2022-09-15",
    "2022-10-30"
]

# grafton_dates = [
#     "2022-04-18",
#     "2022-04-18"
# ]


gardencity_dates = [
    "2022-01-22",
    "2022-01-26",
    "2022-02-11",
    "2022-02-25",
    "2022-03-13",
    "2022-03-25",
    "2022-04-24",
    "2022-05-04",
    "2022-05-10",
    "2022-05-20"
]

random.shuffle(grafton_dates)
random.shuffle(gardencity_dates )

half_grafton = len(grafton_dates) // 2
half_gardencity = len(gardencity_dates) // 2

grafton_val = grafton_dates[:half_grafton]
grafton_val.append('2022-04-06')
grafton_test = grafton_dates[half_grafton:]
grafton_test.append('2022-09-13')

gardencity_val = gardencity_dates[:half_gardencity]

gardencity_val.append('2022-04-06')

gardencity_test = gardencity_dates[half_gardencity:]


desired_pairs_val= [('Grafton', date) for date in grafton_val] + [('GardenCity', date) for date in gardencity_val]
desired_pairs_test = [('Grafton', date) for date in grafton_test] + [('GardenCity', date) for date in gardencity_test]


