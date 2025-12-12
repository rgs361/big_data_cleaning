"""
Script to combine all normalized events with parent categories into a single JSON file.
Output schema:
- Name
- DateTime
- Category (mapped from parent_category)
- Latitude
- Longitude
- Address
"""

import json
import os

def combine_events():
    input_dir = 'event_data_with_parent_categories'
    output_file = 'all_events_combined.json'
    
    files_map = [
        {
            'filename': 'eventbrite_events_normalized.json',
            'mapping': {
                'Name': 'Title',
                'DateTime': 'DateTime',
                'Category': 'parent_category',
                'Latitude': 'lat',
                'Longitude': 'lng',
                'Address': 'Location'
            }
        },
        {
            'filename': 'meetup_events_normalized.json',
            'mapping': {
                'Name': 'Title',
                'DateTime': 'DateTime',
                'Category': 'parent_category',
                'Latitude': 'lat',
                'Longitude': 'lng',
                'Address': 'Location'
            }
        },
        {
            'filename': 'nyc_park_events_normalized.json',
            'mapping': {
                'Name': 'title',
                'DateTime': 'DateTime',
                'Category': 'parent_category',
                'Latitude': 'lat',
                'Longitude': 'lng',
                'Address': 'location'
            }
        },
        {
            'filename': 'permitted_events_normalized.json',
            'mapping': {
                'Name': 'title',
                'DateTime': 'DateTime',
                'Category': 'parent_category',
                'Latitude': 'lat',
                'Longitude': 'lng',
                'Address': 'location'
            }
        }
    ]
    
    all_events = []
    
    for file_info in files_map:
        filepath = os.path.join(input_dir, file_info['filename'])
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found. Skipping.")
            continue
            
        print(f"Processing {file_info['filename']}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        mapping = file_info['mapping']
        count = 0
        
        for item in data:
            # Create new event object with standardized fields
            new_event = {
                'Name': item.get(mapping['Name']),
                'DateTime': item.get(mapping['DateTime']),
                'Category': item.get(mapping['Category']),
                'Latitude': item.get(mapping['Latitude']),
                'Longitude': item.get(mapping['Longitude']),
                'Address': item.get(mapping['Address'])
            }
            
            # Optional: Filter out events with missing critical data if needed
            # For now, we keep everything as requested, but maybe skip if no lat/lng?
            # User didn't specify filtering, so we keep all.
            
            all_events.append(new_event)
            count += 1
            
        print(f"Added {count} events from {file_info['filename']}")

    print(f"Total events combined: {len(all_events)}")
    print(f"Writing to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_events, f, indent=4)
        
    print("Done.")

if __name__ == "__main__":
    combine_events()
