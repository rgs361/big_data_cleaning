"""
Script to transform eventbrite_events.json into a CSV file for Geocodio geocoding.

This creates a Single-Column Format CSV with:
- id: The original index in the JSON array (for mapping results back)
- address: The full address string for geocoding

Eventbrite format: "Borough/City · Venue/Address"
Transformed to: "Venue/Address, Borough/City, NY"
"""

import json
import csv

# Load the eventbrite events from event_data folder
with open('event_data/eventbrite_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Invalid address patterns to skip
INVALID_PATTERNS = ['tba', '00:00', 'online', 'virtual']

# Prepare data for CSV
geocodio_data = []
skipped_count = 0

for idx, event in enumerate(events):
    location = event.get('location', '').strip()
    
    # Skip empty locations
    if not location:
        skipped_count += 1
        continue
    
    # Check if location contains the separator
    if ' · ' not in location:
        skipped_count += 1
        continue
    
    # Split on the separator: "City · Address/Venue"
    parts = location.split(' · ', 1)
    if len(parts) != 2:
        skipped_count += 1
        continue
    
    city_or_borough = parts[0].strip()
    address_or_venue = parts[1].strip()
    
    # Skip invalid addresses
    if address_or_venue.lower() in INVALID_PATTERNS or not address_or_venue:
        skipped_count += 1
        continue
    
    # Transform to Geocodio format: "Address/Venue, City/Borough, NY"
    geocodio_address = f"{address_or_venue}, {city_or_borough}, NY"
    
    # Add the event with its original index for later mapping
    geocodio_data.append({
        'id': idx,
        'address': geocodio_address
    })

# Write to CSV in Single-Column Format with header
output_file = 'event_data_geocodio/eventbrite_pre_geocodio.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'address'])
    writer.writeheader()
    writer.writerows(geocodio_data)

print(f"✅ Created '{output_file}' with {len(geocodio_data)} addresses")
print(f"   (Skipped {skipped_count} invalid/empty locations)")
print(f"\n📋 Next steps:")
print(f"   1. Upload '{output_file}' to Geocodio")
print(f"   2. Select 'address' as the single-column address field")
print(f"   3. Download the geocoded results as 'event_data_geocodio/eventbrite_geocodio.csv'")
print(f"   4. Use the 'id' column to map lat/lng back to your original events")
