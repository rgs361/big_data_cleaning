"""
Script to transform nyc_park_events.json into a CSV file for Geocodio geocoding.

This creates a Single-Column Format CSV with:
- id: The original index in the JSON array (for mapping results back)
- address: The full address string for geocoding

NYC Parks format varies but typically ends with a borough name.
We append ", NY" if not already present.
"""

import json
import csv
import re

# Load the nyc park events from event_data folder
with open('event_data/nyc_park_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# NYC Boroughs - these are valid location endings
NYC_BOROUGHS = ['manhattan', 'brooklyn', 'queens', 'bronx', 'the bronx', 'staten island']

# Patterns to skip
SKIP_PATTERNS = ['virtual', 'online', 'tba', 'tbd']

def normalize_address(location):
    """
    Normalize the address for Geocodio.
    - Skip virtual/online events
    - Append NY if not already present
    """
    if not location:
        return None
    
    location = location.strip()
    location_lower = location.lower()
    
    # Skip virtual/online events
    for pattern in SKIP_PATTERNS:
        if pattern in location_lower:
            return None
    
    # Check if NY is already in the address
    has_ny = bool(re.search(r'\bny\b', location_lower)) or 'new york' in location_lower
    
    if has_ny:
        # Already has NY/New York, return as is
        return location
    
    # Check if it ends with a borough name
    for borough in NYC_BOROUGHS:
        if location_lower.endswith(borough):
            # Append NY after the borough
            return location + ', NY'
    
    # Doesn't end with borough and no NY - append New York, NY
    return location + ', New York, NY'

# Prepare data for CSV
geocodio_data = []
skipped_count = 0

for idx, event in enumerate(events):
    location = event.get('location', '').strip()
    
    normalized = normalize_address(location)
    
    if normalized is None:
        skipped_count += 1
        continue
    
    # Add the event with its original index for later mapping
    geocodio_data.append({
        'id': idx,
        'address': normalized
    })

# Write to CSV in Single-Column Format with header
output_file = 'event_data_geocodio/nyc_park_pre_geocodio.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'address'])
    writer.writeheader()
    writer.writerows(geocodio_data)

print(f"✅ Created '{output_file}' with {len(geocodio_data)} addresses")
print(f"   (Skipped {skipped_count} virtual/invalid locations)")
print(f"\n📋 Next steps:")
print(f"   1. Upload '{output_file}' to Geocodio")
print(f"   2. Select 'address' as the single-column address field")
print(f"   3. Download the geocoded results as 'event_data_geocodio/nyc_park_geocodio.csv'")
print(f"   4. Use the 'id' column to map lat/lng back to your original events")
