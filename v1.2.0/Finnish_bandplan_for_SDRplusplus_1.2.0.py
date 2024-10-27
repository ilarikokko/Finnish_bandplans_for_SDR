import requests
import json
import sys
from collections import defaultdict

# API URL
url = "https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin"

# SDR++ Bandplan template
sdr_bandplan = {
    "name": "Finland",
    "country_name": "Finland",
    "country_code": "FI",
    "author_name": "Traficom",
    "author_url": "https://opendata.traficom.fi/api/v13/Taajuusjakotaulukko_fin",
    "bands": []
}

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
    intervals = []
    
    # Parse data into interval structures
    for item in data:
        start_freq = int(item["Osa_alue_alaraja__Hz_"])
        end_freq = int(item["Osa_alue_yläraja__Hz_"])
        usage_name = item.get("Osakaistan_käyttö", "Unknown")
        intervals.append((start_freq, end_freq, usage_name))
    
    # Sort intervals by start frequency
    intervals.sort()
    
    merged_intervals = []
    all_points = set()
    
    # Break down intervals into distinct start and end points
    for start, end, usage_name in intervals:
        all_points.add(start)
        all_points.add(end)
    
    all_points = sorted(all_points)
    
    # Construct non-overlapping intervals
    for i in range(len(all_points) - 1):
        start, end = all_points[i], all_points[i + 1]
        usage_names = [name for s, e, name in intervals if s < end and e > start]
        usage_names = " | ".join(sorted(set(usage_names)))
        
        if usage_names:
            merged_intervals.append({
                "name": usage_names,
                "type": "other",
                "start": start,
                "end": end
            })
    
    # Additional merging of consecutive intervals with the same name and type
    consolidated_intervals = []
    for band in merged_intervals:
        if consolidated_intervals and \
           consolidated_intervals[-1]["name"] == band["name"] and \
           consolidated_intervals[-1]["type"] == band["type"] and \
           consolidated_intervals[-1]["end"] == band["start"]:
            # Extend the end frequency of the last interval
            consolidated_intervals[-1]["end"] = band["end"]
        else:
            consolidated_intervals.append(band)
    
    return consolidated_intervals

def save_to_json(bands):
    # Save parsed bands into SDR++ format
    sdr_bandplan["bands"] = bands
    with open("finland.json", "w", encoding="utf-8") as f:
        json.dump(sdr_bandplan, f, indent=4, ensure_ascii=False)
    print("Bandplan saved to 'finland.json'.")

# Fetch, parse, and save bandplan
data = fetch_bandplan()
if data:  # Only parse and save if data is not empty
    parsed_bands = parse_bandplan(data)
    save_to_json(parsed_bands)

# End of script message
input("Press any key to exit...")