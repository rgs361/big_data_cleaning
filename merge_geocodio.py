"""
Script to merge geocoded lat/lng from Geocodio CSV back into meetup_events.json.
Uses the 'id' column to map coordinates to the correct event.
"""

import json
import csv

# Load the original meetup events from event_data folder
with open('event_data/meetup_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Load the geocoded CSV from event_data_geocodio folder and build a mapping of id -> (lat, lng)
coords_map = {}
with open('event_data_geocodio/meetup_geocodio.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        event_id = int(row['id'])
        lat = row.get('Geocodio Latitude', '').strip()
        lng = row.get('Geocodio Longitude', '').strip()
        
        # Only add if we have valid coordinates
        if lat and lng:
            coords_map[event_id] = (float(lat), float(lng))

# Merge coordinates back into events
geocoded_count = 0
for idx, event in enumerate(events):
    if idx in coords_map:
        event['lat'] = coords_map[idx][0]
        event['lng'] = coords_map[idx][1]
        geocoded_count += 1
    else:
        # No coordinates found - set to None
        event['lat'] = None
        event['lng'] = None

# Save the updated events to event_data_latlng folder
with open('event_data_latlng/meetup_events_latlng.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, indent=4, ensure_ascii=False)

print(f"✅ Created event_data_latlng/meetup_events_latlng.json")
print(f"   - {geocoded_count} events with coordinates")
print(f"   - {len(events) - geocoded_count} events without coordinates (online/not geocoded)")
