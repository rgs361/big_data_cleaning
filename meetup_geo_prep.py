"""
Script to transform meetup_events.json into a CSV file for Geocodio geocoding.

This creates a Single-Column Format CSV with:
- id: The original index in the JSON array (for mapping results back)
- address: The full address string for geocoding

After geocoding with Geocodio, you can use the 'id' column to map 
latitude/longitude coordinates back to the original events.
"""

import json
import csv

# Load the meetup events from event_data folder
with open('event_data/meetup_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Prepare data for CSV
geocodio_data = []

for idx, event in enumerate(events):
    location = event.get('Location', '').strip()
    
    # Skip online events or empty locations - can't geocode these
    if not location or location.lower().startswith('online'):
        continue
    
    # Check for NY/New York context and append if needed
    location_lower = location.lower()
    has_ny = 'ny' in location_lower.split() or location_lower.endswith('ny') or ', ny' in location_lower
    has_new_york = 'new york' in location_lower
    
    if has_new_york and not has_ny:
        # Has "New York" but not "NY" - append NY
        location = location + ', NY'
    elif not has_new_york and not has_ny:
        # Has neither - append full location context
        location = location + ', New York, NY'
    # If has NY (with or without New York), leave as is
    
    # Add the event with its original index for later mapping
    geocodio_data.append({
        'id': idx,
        'address': location
    })

# Write to CSV in Single-Column Format with header
output_file = 'event_data_geocodio/meetup_pre_geocodio.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'address'])
    writer.writeheader()
    writer.writerows(geocodio_data)

print(f"✅ Created '{output_file}' with {len(geocodio_data)} addresses")
print(f"   (Skipped {len(events) - len(geocodio_data)} online/empty locations)")
print(f"\n📋 Next steps:")
print(f"   1. Upload '{output_file}' to Geocodio")
print(f"   2. Select 'address' as the single-column address field")
print(f"   3. Download the geocoded results to 'event_data_geocodio/'")
print(f"   4. Use the 'id' column to map lat/lng back to your original events")
