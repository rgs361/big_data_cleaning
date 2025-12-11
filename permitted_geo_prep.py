"""
Script to transform permitted_events.json into a CSV file for Geocodio geocoding.

This creates a Single-Column Format CSV with:
- id: The original index in the JSON array (for mapping results back)
- address: The full address string for geocoding

Permitted events format: "Park Name: Specific Location"
We extract the park name and append "New York, NY" for geocoding.
"""

import json
import csv
import re

# Load the permitted events from event_data folder
with open('event_data/permitted_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Patterns to skip
SKIP_PATTERNS = ['virtual', 'online', 'tba', 'tbd']

def normalize_address(location):
    """
    Normalize the address for Geocodio.
    - Extract park name from "Park Name: Specific Location" format
    - Handle multiple locations separated by commas
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
    
    # If there are multiple locations (comma-separated), take just the first one
    if ',' in location:
        location = location.split(',')[0].strip()
    
    # Extract the park name (before the colon) if present
    if ':' in location:
        park_name = location.split(':')[0].strip()
    else:
        park_name = location
    
    # Check if NY/New York is already in the address
    park_lower = park_name.lower()
    has_ny = bool(re.search(r'\bny\b', park_lower)) or 'new york' in park_lower
    
    if has_ny:
        return park_name
    
    # Append New York, NY for geocoding context
    return f"{park_name}, New York, NY"

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
output_file = 'event_data_geocodio/permitted_pre_geocodio.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'address'])
    writer.writeheader()
    writer.writerows(geocodio_data)

print(f"✅ Created '{output_file}' with {len(geocodio_data)} addresses")
print(f"   (Skipped {skipped_count} virtual/invalid locations)")
print(f"\n📋 Next steps:")
print(f"   1. Upload '{output_file}' to Geocodio")
print(f"   2. Select 'address' as the single-column address field")
print(f"   3. Download the geocoded results as 'event_data_geocodio/permitted_geocodio.csv'")
print(f"   4. Use the 'id' column to map lat/lng back to your original events")
