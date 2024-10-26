# Finnish Bandplan for the SDR Software

## What is it?
This repository contains Python scripts and their corresponding Windows executables for fetching and creating bandplans from the Finnish Traficom API for use with SDR++ and SDR# software. The scripts fetch bandplan data, process it, and save it in the appropriate formats for each software.

## Files & how to use
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
- **No additional libraries are required for the executables**; they are standalone and bundled with the necessary dependencies.

## API Used
Both scripts fetch data from the Finnish Traficom API:
- **API URL**: https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin

## Notes
- Ensure you have an internet connection when running the scripts or the executables, as they require access to the API to fetch data.
- If you encounter any issues or have questions, feel free to open an issue in this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
