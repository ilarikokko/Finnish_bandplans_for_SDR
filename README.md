# Finnish Traficom Bandplan for the SDR Software

## What is it?
This repository contains Python scripts and their corresponding Windows executables for fetching and creating bandplans from the Finnish Traficom API for use with SDR++ and SDR# software. The scripts fetch bandplan data, process it, and save it in the appropriate formats for each software.

**There are also ready-made files, so you don't have to use scripts if you don't want to!** 

I added the scripts to this repository just because, I don't know how often Traficom updates the frequency distribution table (maybe once every ten years :D?).

## Ready-made files & where to put them
### When using SDR++ (Windows)
1. Download [finland.json](https://github.com/ilarikokko/Finnish_bandplans_for_SDR/releases/download/v1.2.0/finland.json).
2. Move the file to the `\res\bandplans\` folder (Here you should find other countries json files).
3. Open the software and change the Band Plan to "Finland"
4. Done!

### When using SDR# (Windows)
1. Download [BandPlan.xml](https://github.com/ilarikokko/Finnish_bandplans_for_SDR/releases/download/v1.2.0/BandPlan.xml).
2. Go to the root folder of the SDR# (Same folder where you can find the SDRSharp.exe).
3. Make a backup of the original band plan file or rename it something like this `BandPlan.backup`.
4. Move the `BandPlan.xml` file to this folder.
5. Open the software.
6. Done!

### Example SDR++
![sdrpp](https://github.com/user-attachments/assets/6e351a5f-39e0-42b9-8f86-865da88fddcc)

### Example SDR#
![sdrsharp](https://github.com/user-attachments/assets/adfe46fa-1004-491c-828f-72e201de1549)


## Python scripts, EXE files & how to use them?
### 1. Finnish_bandplan_for_SDRplusplus_1.2.0.py
- **Description**: The "Linux" Python version of the SDR++ bandplan script.
- **Usage**:
    - Run the script in a Python environment `python3 ./Finnish_bandplan_for_SDRplusplus_1.2.0.py` with the required libraries installed (read "Requirements for Python scripts").
    - The output will be saved as `finland.json`.

### 2. Finnish_bandplan_for_SDRplusplus_1.2.0.exe
- **Description**: The Windows executable version of the SDR++ bandplan script.
- **Usage**:
    - Double-click the executable to run it. 
    - A terminal window will open, showing the progress of fetching and processing the bandplan. 
    - The output will be saved as `finland.json`.

### 3. Finnish_bandplan_for_SDRsharp_1.2.0.py
- **Description**:The "Linux" Python version of the SDR# bandplan script.
- **Usage**:
    - Run the script in a Python environment `python3 ./Finnish_bandplan_for_SDRsharp_1.2.0.py` with the required libraries installed (read "Requirements for Python scripts").
    - The output will be saved as `BandPlan.xml`.

### 4. Finnish_bandplan_for_SDRsharp_1.2.0.exe
- **Description**: The Windows executable version of the SDR# bandplan script.
- **Usage**:
    - Double-click the executable to run it.
    - A terminal window will open, showing the progress of fetching and processing the bandplan.
    - The output will be saved as `BandPlan.xml`.

## How are the EXE files made and what do they contain?
- Both exe's are based of provided Python scripts.
- Both EXE files are made with [PyInstaller](https://pyinstaller.org/en/stable/)
- In my case, the exact commands were:
    - `python -m PyInstaller --onefile --name "Finnish_bandplan_for_SDRplusplus_1.2.0" .\Finnish_bandplan_for_SDRplusplus_1.2.0.py`
    - `python -m PyInstaller --onefile --name "Finnish_bandplan_for_SDRsharp_1.2.0" .\Finnish_bandplan_for_SDRsharp_1.2.0.py`

## Requirements for Python scripts
- **Python**: Make sure you have Python installed if you plan to run the `.py` scripts. The scripts require the `requests` library. You can install it using:
    ```bash
    pip install requests
    ```

## API
Both scripts fetch data from the Traficom public API:
- **API URL**: https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin

## Notes
- Ensure you have an internet connection when running the scripts or the executables, as they require access to the API to fetch data.
- If you encounter any issues or have questions, feel free to open an issue in this repository.

## Changelog:
- v1.2.0 (Current version)
    - **Non-Overlapping Frequency Splitting:**
    Added a function to handle overlapping frequency ranges by splitting them into non-overlapping sub-ranges.
    This ensures that multiple usage types are represented in each range without overlapping.

    - **Usage Type Separator Update:**
    Modified the output format to display multiple usage types with a | separator instead of a comma (,).
  
    - **Merged Continuous Bands:**
    Enhanced the scripts to merge consecutive frequency bands that share the same usage type(s) into a single continuous range.
    For example, adjacent bands with the same usage are now consolidated into one band entry instead of being represented as separate blocks.

- v1.0.0
    -  Initial release


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
