import pandas as pd
import os
from glob import glob

# Directory containing CSV files
folder = r"excel_AIS\processed_excel_AIS"
folder = r"excel_AIS\cmmi_data_all"

# Get all CSV files in the folder
csv_files = glob(os.path.join(folder, "*.csv"))

# Dictionary to store combined dataframes per deployment
deployments = {}

for file in csv_files:
    # Extract deployment ID from filename (first number)
    basename = os.path.basename(file)
    deployment_id = basename.split('_')[0]
    if "SHARE" not in file:
        continue
    # Load CSV
    df = pd.read_csv(file)

    # Add to the dictionary
    if deployment_id in deployments:
        deployments[deployment_id] = pd.concat([deployments[deployment_id], df], ignore_index=True)
    else:
        deployments[deployment_id] = df

# # Dictionary to store unique ship types per deployment
unique_ship_types = {}

for deployment_id, df in deployments.items():
    if 'type' in df.columns:
        unique_types = df['type'].dropna().unique()
        unique_ship_types[deployment_id] = unique_types

# Print results
for deployment_id, ship_types in unique_ship_types.items():
    print(f"Deployment {deployment_id}:")
    for stype in ship_types:
        print(f"  - {stype}")
    print()


# Dictionary to store counts per deployment
ship_type_counts = {}

for deployment_id, df in deployments.items():
    if 'type' in df.columns and 'mmsi' in df.columns:
        counts = df.groupby('type')['mmsi'].nunique()
        ship_type_counts[deployment_id] = counts

# Print results
for deployment_id, counts in ship_type_counts.items():
    print(f"Deployment {deployment_id}:")
    print(counts)
    print()



# Example: save combined deployment CSVs
for deployment_id, df in deployments.items():
    df.to_csv(os.path.join(rf"data\dataset_AIS_full_no_distance_filter", f"ais_{deployment_id}_combined_share.csv"), index=False)

print("Done! Combined files created per deployment with renamed MMSI.")