# AIS Annotator & WAV Processing Pipeline

## Overview
This project contains scripts to process AIS (Automatic Identification System) data, extract vessel information, generate audio snippets from hydrophone recordings. (and create spectrogram and distance-vs-time plots for vessel monitoring if HMD also present).

Main functionalities:
1. AIS Data Processing: Load, filter, and calculate vessel distances from hydrophones.
2. Closest Ship Detection: Identify the closest vessels at each timestamp.
3. Audio Extraction: Trim hydrophone recordings into 10-second snippets for analysis.
4. Plot Generation: Produce spectrograms and distance-vs-time plots for vessel activity visualization.
5. Database Creation: Generate CSV files summarizing vessel information and distances.

## Folder Structure
```
AIS_annotator/
├── create_figures_or_wavs/
│   ├── Create_Excel_Database.py
│   ├── Create_Database_AIS_2_SHIPS_and_Sound.py
│   ├── Merge_excel_files.py
├── utils/
│   ├── __init__.py
│   ├── import_data.py
│   ├── audio_vessel_annotator.py
│   ├── distance_calculator.py
│   ├── find_closest_wav.py
│   ├── plot_spectrogram_distance.py
│   ├── data_processing_utils.py
excel_AIS/
├── raw_excel_AIS/
├── cmmi_data_all/
Create_Database_AIS_and_Sound.py
hybrid_millidecade_bands/
data/
├── data_per_station_...
plots_per_station_...
database.csv
```

## Installation
1. Clone the repository:  
   `git clone <repository_url>`
2. Install Python 3.9+.
3. Create a virtual environment:  
   `python -m venv envi`
4. Activate the environment:  
   Windows: `envi\Scripts\activate`  
   Linux/macOS: `source envi/bin/activate`
5. Install required packages:  
   `pip install -r requirements.txt`

## Scripts

### 1. AIS Database Creation
- `Create_Excel_Database.py`: Processes AIS Excel files and calculates vessel distances.
- `Create_Database_AIS_and_Sound.py`: Generates WAV snippets and database for single ships.
- `Create_Database_AIS_2_SHIPS_and_Sound.py`: Generates WAV snippets and database for closest two ships.

### 2. WAV Snippet Generation
- `trim_wav()` function: Extracts 10-second snippets from hydrophone recordings with optional overlap.

### 3. Plotting & Analysis
- `plot_spectrogram_distance.py`: Creates long-term spectrograms and distance-vs-time plots.  
- Key functions:
  - `find_and_open_xr_dataset()`: Locate and open NetCDF files for spectrogram data.
  - `create_and_save_distance_vs_time_plot()`: Plot vessel distances and predictions.
  - `save_plot()`: Save plots with consistent size and formatting.
  - `plot_analysis()`: High-level function to generate plots for each day of deployment.

### 4. Data Merging
- `Merge_excel_files.py`: Combine multiple AIS CSV files per deployment and analyze unique vessel types.

## Usage
1. Place raw AIS Excel files in `excel_AIS/raw_excel_AIS/`.
2. Place processed AIS CSV files (if already created) in `excel_AIS/cmmi_data_all/`.
3. Place hydrophone millidecade bands (if exist) in `hybrid_millidecade_bands/`.
4. Place raw data in raw_data_folder `PhD_Clea`
5. Run the desired script:
   - Single ship database: `python Create_Database_AIS_and_Sound.py`
   - Two ship database: `python Create_Database_AIS_2_SHIPS_and_Sound.py`
   - Generate plots: handled automatically in the above scripts. 
6. Output:
   - WAV snippets saved in `data/data_per_station_*`.
   - Plots saved in `plots_per_station_*`.
   - Databases saved in `database.csv` (single ship) or `UC6/database.csv` (two ships).

## Configuration
- Default window size and comment are extracted from `config.yaml`.
- Example config entries:
```yaml
seed: 42
default_window_size: 6
custom_window_size:
  '29187': 5
  '28434': 5
exclude_deployments:
  - '26982'
  - '15812'
  - '25712'

paths:
  base_directory: 'excel_AIS\\raw_excel_AIS'
  csv_location: 'excel_AIS\\processed_excel_AIS'
  search_directory: 'hybrid_millidecade_bands'
  raw_data_folder: 'PhD_Clea'

```

## Dependencies
- Python 3.9+
- numpy
- pandas
- matplotlib
- xarray
- pypam
- pydub
- tqdm

## License
MIT License

## Contact
For questions or support, contact: [wout decrop] <wout.decrop@vliz.be>
