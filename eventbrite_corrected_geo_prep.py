"""
Script to transform eventbrite_events_corrected.json into a CSV file for Geocodio geocoding.

This creates a Single-Column Format CSV with:
- id: The EventID (for mapping results back)
- address: The full address string for geocoding
"""

import json
import csv
import os

# Ensure output directory exists
os.makedirs('event_data_geocodio', exist_ok=True)

# Load the corrected eventbrite events
input_path = 'event_data/eventbrite_events_corrected.json'
output_path = 'event_data_geocodio/eventbrite_corrected_geocodio_input.csv'

print(f"Reading from {input_path}...")
with open(input_path, 'r', encoding='utf-8') as f:
    events = json.load(f)

# Invalid address patterns to skip
INVALID_PATTERNS = ['tba', '00:00', 'online', 'virtual', 'to be announced']

# Prepare data for CSV
geocodio_data = []
skipped_count = 0

for event in events:
    event_id = event.get('EventID')
    location = event.get('Location')
    
    # Skip if missing ID or location
    if not event_id or not location:
        skipped_count += 1
        continue
        
    location_clean = location.strip()
    location_lower = location_clean.lower()
    
    # Check for invalid patterns
    is_invalid = False
    for pattern in INVALID_PATTERNS:
        if pattern in location_lower:
            is_invalid = True
            break
            
    if is_invalid:
        skipped_count += 1
        continue

    # The location in this file seems to be a full address already
    # e.g., "151 Mulberry Street, New York, NY 10013"
    # So we can use it directly.
    
    geocodio_data.append({
        'id': event_id,
        'address': location_clean
    })

# Write to CSV
print(f"Writing {len(geocodio_data)} records to {output_path}...")
print(f"Skipped {skipped_count} records due to missing or invalid location.")

with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'address'])
    writer.writeheader()
    writer.writerows(geocodio_data)

print("Done.")
