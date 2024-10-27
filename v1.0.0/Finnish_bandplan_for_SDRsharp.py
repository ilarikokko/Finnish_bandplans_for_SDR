import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
import sys

# API URL
url = "https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin"

# XML template for SDR# bandplan
sdr_bandplan = ET.Element("ArrayOfRangeEntry", {
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xmlns:xsd": "http://www.w3.org/2001/XMLSchema"
})

def fetch_bandplan():
    # Make the API request
    print("Fetching bandplan from Traficom API: https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)

        if response.status_code == 200:
            print("Bandplan fetched successfully.")
            response.encoding = 'utf-8'  # Ensure UTF-8 encoding
            return response.json().get("value", [])
        else:
            print(f"Unexpected status code: {response.status_code}")
            sys.exit(1)  # Exit with code 1 for unexpected status

    except requests.exceptions.RequestException as e:
        print(f"Error fetching bandplan: {e}")
        sys.exit(1)  # Exit with code 1 for request error

def parse_bandplan(data):
    band_dict = defaultdict(list)

    for item in data:
        # Convert frequencies to Hz for uniform comparison
        start_freq = int(item["Osa_alue_alaraja__Hz_"])
        end_freq = int(item["Osa_alue_yläraja__Hz_"])
        usage_name = item.get("Osakaistan_käyttö", "Unknown")

        # Store data with start, end, and usage name
        band_dict[usage_name].append({
            "start": start_freq,
            "end": end_freq,
            "usage_name": usage_name
        })

    filtered_bands = []

    # Filter out overlapping ranges
    for usage_name, bands in band_dict.items():
        # Sort by start frequency, and then by range length in descending order
        bands.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))

        non_overlapping_bands = []
        for band in bands:
            # Only add if it does not fall completely within any already added range
            if not any(existing["start"] <= band["start"] and existing["end"] >= band["end"]
                       for existing in non_overlapping_bands):
                non_overlapping_bands.append(band)

        # Add unique non-overlapping bands to the final list
        for band in non_overlapping_bands:
            filtered_bands.append({
                "name": usage_name,
                "start": band["start"],
                "end": band["end"]
            })

    return filtered_bands

def save_to_xml(bands):
    # Generate XML entries for each band
    for band in bands:
        range_entry = ET.SubElement(sdr_bandplan, "RangeEntry")
        range_entry.set("minFrequency", str(band["start"]))
        range_entry.set("maxFrequency", str(band["end"]))
        range_entry.set("color", "90FF0000")  # Default color, modify if necessary
        range_entry.set("mode", "AM")  # Default mode, modify as needed
        range_entry.set("step", "1000")  # Default step, modify as needed
        range_entry.text = band["name"]

    # Write XML data to file
    tree = ET.ElementTree(sdr_bandplan)
    with open("BandPlan.xml", "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    print("Bandplan saved to 'BandPlan.xml'.")

# Fetch, parse, and save bandplan
data = fetch_bandplan()
if data:  # Only parse and save if data is not empty
    parsed_bands = parse_bandplan(data)
    save_to_xml(parsed_bands)

# End of script message
input("Press any key to exit...")
