"""
Script to merge Geocodio results back into the corrected Eventbrite JSON.
Output is saved to event_data_normalized/eventbrite_events_normalized.json.
"""

import json
import csv
import os

# Ensure output directory exists
os.makedirs('event_data_normalized', exist_ok=True)

json_path = 'event_data/eventbrite_events_corrected.json'
csv_path = 'event_data_geocodio/eventbrite_corrected_geocodio.csv'
output_path = 'event_data_normalized/eventbrite_events_normalized.json'

print(f"Loading JSON from {json_path}...")
with open(json_path, 'r', encoding='utf-8') as f:
    events = json.load(f)

# Create a lookup dictionary from the CSV
# id -> {lat, lng}
geo_lookup = {}

print(f"Loading CSV from {csv_path}...")
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        event_id = row.get('id')
        lat = row.get('Geocodio Latitude')
        lng = row.get('Geocodio Longitude')
        
        if event_id and lat and lng:
            try:
                geo_lookup[event_id] = {
                    'lat': float(lat),
                    'lng': float(lng)
                }
            except ValueError:
                continue

# Merge coordinates into events
merged_count = 0
for event in events:
    event_id = event.get('EventID')
    if event_id in geo_lookup:
        event['lat'] = geo_lookup[event_id]['lat']
        event['lng'] = geo_lookup[event_id]['lng']
        merged_count += 1
    else:
        event['lat'] = None
        event['lng'] = None

print(f"Merged coordinates for {merged_count} events.")
print(f"Writing to {output_path}...")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(events, f, indent=4)

print("Done.")
