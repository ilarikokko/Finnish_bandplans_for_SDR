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
        sys.exit(1)

def parse_bandplan(data):
    intervals = []
    
    for item in data:
        start_freq = int(item["Osa_alue_alaraja__Hz_"])
        end_freq = int(item["Osa_alue_yläraja__Hz_"])
        usage_name = item.get("Osakaistan_käyttö", "Unknown")
        intervals.append((start_freq, end_freq, usage_name))
    
    intervals.sort()
    
    merged_intervals = []
    all_points = set()
    
    for start, end, usage_name in intervals:
        all_points.add(start)
        all_points.add(end)
    
    all_points = sorted(all_points)
    
    for i in range(len(all_points) - 1):
        start, end = all_points[i], all_points[i + 1]
        usage_names = [name for s, e, name in intervals if s < end and e > start]
        usage_names = " | ".join(sorted(set(usage_names)))  # Use '|' as separator
        
        if usage_names:
            merged_intervals.append({
                "name": usage_names,
                "start": start,
                "end": end
            })
    
    consolidated_intervals = []
    for band in merged_intervals:
        if consolidated_intervals and \
           consolidated_intervals[-1]["name"] == band["name"] and \
           consolidated_intervals[-1]["end"] == band["start"]:
            consolidated_intervals[-1]["end"] = band["end"]
        else:
            consolidated_intervals.append(band)
    
    return consolidated_intervals

def save_to_xml(bands):
    # Generate XML entries for each band
    for band in bands:
        range_entry = ET.SubElement(sdr_bandplan, "RangeEntry")
        range_entry.set("minFrequency", str(band["start"]))
        range_entry.set("maxFrequency", str(band["end"]))
        range_entry.set("color", "90FF0000")
        range_entry.set("mode", "AM")
        range_entry.set("step", "1000")
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
