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
                "type": "other",
                "start": band["start"],
                "end": band["end"]
            })
    
    return filtered_bands

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