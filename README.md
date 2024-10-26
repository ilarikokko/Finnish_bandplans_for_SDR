# Finnish Traficom Bandplan for the SDR Software

## What is it?
This repository contains Python scripts and their corresponding Windows executables for fetching and creating bandplans from the Finnish Traficom API for use with SDR++ and SDR# software. The scripts fetch bandplan data, process it, and save it in the appropriate formats for each software.

**There are also ready-made files, so you don't have to use scripts if you don't want to!** I added the scripts to this repository just because, I don't know how often Traficom updates the frequency distribution table (maybe once every ten years :D?).

## Ready-made files & where to put them
### When using SDR++ (Windows)
1. Download [finland.json](https://github.com/ilarikokko/Finnish_bandplans_for_SDR/releases/download/v1.0.0/finland.json).
2. Move the file to the `\res\bandplans\` folder (Here you should find other countries json files).
3. Open the software and change the Band Plan to "Finland"
4. Done!

### When using SDR# (Windows)
1. Download [BandPlan.xml](https://github.com/ilarikokko/Finnish_bandplans_for_SDR/releases/download/v1.0.0/BandPlan.xml).
2. Go to the root folder of the SDR# (Same folder where you can find the SDRSharp.exe).
3. Make a backup of the original band plan file or rename it something like this `BandPlan.backup`.
4. Move the `BandPlan.xml` file to this folder.
5. Open the software.
6. Done!

### SDR++
![sdrpp](https://github.com/user-attachments/assets/6e351a5f-39e0-42b9-8f86-865da88fddcc)

### SDR#
![sdrsharp](https://github.com/user-attachments/assets/adfe46fa-1004-491c-828f-72e201de1549)


## Script files and how to use them
### 1. Finnish_bandplan_for_SDRplusplus.py
- **Description**: The "Linux" Python version of the SDR++ bandplan script.
- **Usage**:
    - Run the script in a Python environment `python3 ./Finnish_bandplan_for_SDRplusplus.py` with the required libraries installed (read Requirements for Python scripts).
    - The output will be saved as `finland.json`.

### 2. Finnish_bandplan_for_SDRplusplus.exe
- **Description**: The Windows executable version of the SDR++ bandplan script.
- **Usage**:
    - Double-click the executable to run it. 
    - A terminal window will open, showing the progress of fetching and processing the bandplan. 
    - The output will be saved as `finland.json`.

### 3. Finnish_bandplan_for_SDRsharp.py
- **Description**:The "Linux" Python version of the SDR# bandplan script.
- **Usage**:
    - Run the script in a Python environment `python3 ./Finnish_bandplan_for_SDRsharp.py` with the required libraries installed (read Requirements for Python scripts).
    - The output will be saved as `BandPlan.xml`.

### 4. Finnish_bandplan_for_SDRsharp.exe
- **Description**: The Windows executable version of the SDR# bandplan script.
- **Usage**:
    - Double-click the executable to run it.
    - A terminal window will open, showing the progress of fetching and processing the bandplan.
    - The output will be saved as `BandPlan.xml`.

## Requirements for Python scripts
- **Python**: Make sure you have Python installed if you plan to run the `.py` scripts. The scripts require the `requests` library. You can install it using:
    ```bash
    pip install requests
    ```

## API Used
Both scripts fetch data from the Finnish Traficom API:
- **API URL**: https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin

## Notes
- Ensure you have an internet connection when running the scripts or the executables, as they require access to the API to fetch data.
- If you encounter any issues or have questions, feel free to open an issue in this repository.

## Known "bugs"
- There is no support in either software for overlapping bands. This is why the texts overlap each other.
- Most of the overlapping has been fixed in the scripts, which removes the duplicate bands. However, there are still many bands that overlap with each other. There is no clear fix for this.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
