# Vessel_Acoustic_Recording_Annotator

## Overview
This project contains scripts to process AIS (Automatic Identification System) data, extract vessel information, generate audio snippets from hydrophone recordings. .

Main functionalities:
1. AIS Data Processing: Load, filter, and calculate vessel distances from hydrophones.
2. Closest Ship Detection: Identify the closest vessels at each timestamp.
3. Audio Extraction: Trim hydrophone recordings into 10-second snippets for analysis.
4. Database Creation: Generate CSV files summarizing vessel information and distances.

Side functionalities:
- Convert FLAC files to WAV files

## Downstream Project

After creating the annotated audio snippets, they can be used directly with the following CLAP-based model for vessel distance categorization:

🔗 **Audio Vessel Distance Categorizer (CLAP)**  
https://github.com/woutdecrop/audio_vessel_distance_categorizer

This model uses the extracted audio snippets to categorize vessel distance classes based on underwater acoustic signatures.

## Folder Structure
```
AIS_annotator/
│   ├── from_FLAC_to_WAV.py
├── utils/
│   ├── __init__.py
│   ├── import_data.py
│   ├── audio_vessel_annotator.py
│   ├── distance_calculator.py
│   ├── find_closest.py
│   ├── data_base_creater.py
│   ├── data_processing_utils.py
excel_AIS/
├── raw_excel_AIS/
├── processed_excel_AIS/
Create_Database_AIS_and_Sound.py
from_FLAC_to_WAV.py
data/
├── data_per_station_...
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

## Usage
1. Place raw AIS Excel files in `excel_AIS/raw_excel_AIS/`.
2. Place processed AIS CSV files (if already created) in `excel_AIS/processed_excel_AIS/`.
3. Place raw data in raw_data_folder `data`
4. Run the desired script:
   - Single ship database: `python Create_Database_AIS_and_Sound.py`
5. Output:
   - WAV snippets saved in `data/data_per_station_*`.
   - Databases saved in `database.csv` 

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
  raw_data_folder: 'data'

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
