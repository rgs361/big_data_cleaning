"""
Script to normalize date/time formats across all event JSONs.

Converts all date formats to Unix timestamps (milliseconds) like meetup_events:
- eventbrite: "Tue, Dec 9 • 6:00 PM" 
- nyc_park_events: "date": "November 28, 2025", "time": "10:00 AM"
- permitted_events: "date": "December 03, 2025", "time": "12:00 AM"

Outputs to event_data_normalized/ folder.
"""

import json
from datetime import datetime
import re

def parse_eventbrite_datetime(date_time_str):
    """
    Parse Eventbrite format: "Tue, Dec 9 • 6:00 PM" or "Tomorrow • 11:00 PM"
    Returns Unix timestamp in milliseconds or None if cannot parse.
    """
    if not date_time_str or date_time_str == "N/A":
        return None
    
    # Remove day of week and split on bullet
    parts = date_time_str.split('•')
    if len(parts) != 2:
        return None
    
    date_part = parts[0].strip()
    time_part = parts[1].strip()
    
    # Skip relative dates like "Tomorrow", "Today", "Saturday"
    relative_terms = ['tomorrow', 'today', 'monday', 'tuesday', 'wednesday', 
                     'thursday', 'friday', 'saturday', 'sunday']
    if any(term in date_part.lower() for term in relative_terms):
        return None
    
    # Remove day of week (e.g., "Tue, " or "Fri, ")
    date_part = re.sub(r'^[A-Za-z]+,?\s*', '', date_part)
    
    try:
        # Combine date and time, assume 2025 if no year
        if ',' in date_part:
            # Has year: "Dec 9, 2025"
            dt_str = f"{date_part} {time_part}"
            dt = datetime.strptime(dt_str, "%b %d, %Y %I:%M %p")
        else:
            # No year: "Dec 9"
            dt_str = f"{date_part}, 2025 {time_part}"
            dt = datetime.strptime(dt_str, "%b %d, %Y %I:%M %p")
        
        # Convert to Unix timestamp in milliseconds
        return int(dt.timestamp() * 1000)
    except:
        return None


def parse_standard_datetime(date_str, time_str):
    """
    Parse standard format: date="November 28, 2025", time="10:00 AM"
    Returns Unix timestamp in milliseconds or None if cannot parse.
    """
    if not date_str or not time_str:
        return None
    
    try:
        dt_str = f"{date_str} {time_str}"
        dt = datetime.strptime(dt_str, "%B %d, %Y %I:%M %p")
        return int(dt.timestamp() * 1000)
    except:
        return None


# Process Eventbrite events
print("Processing Eventbrite events...")
with open('event_data_latlng/eventbrite_events_latlng.json', 'r', encoding='utf-8') as f:
    eventbrite_events = json.load(f)

eventbrite_converted = 0
for event in eventbrite_events:
    date_time = event.get('date_time', '')
    timestamp = parse_eventbrite_datetime(date_time)
    event['DateTime'] = timestamp
    if timestamp:
        eventbrite_converted += 1

with open('event_data_normalized/eventbrite_events_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(eventbrite_events, f, indent=4, ensure_ascii=False)

print(f"✅ Eventbrite: {eventbrite_converted}/{len(eventbrite_events)} events with DateTime")


# Process NYC Park events
print("\nProcessing NYC Park events...")
with open('event_data_latlng/nyc_park_events_latlng.json', 'r', encoding='utf-8') as f:
    nyc_park_events = json.load(f)

nyc_park_converted = 0
for event in nyc_park_events:
    date_str = event.get('date', '')
    time_str = event.get('time', '')
    timestamp = parse_standard_datetime(date_str, time_str)
    event['DateTime'] = timestamp
    if timestamp:
        nyc_park_converted += 1

with open('event_data_normalized/nyc_park_events_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(nyc_park_events, f, indent=4, ensure_ascii=False)

print(f"✅ NYC Park: {nyc_park_converted}/{len(nyc_park_events)} events with DateTime")


# Process Permitted events
print("\nProcessing Permitted events...")
with open('event_data_latlng/permitted_events_latlng.json', 'r', encoding='utf-8') as f:
    permitted_events = json.load(f)

permitted_converted = 0
for event in permitted_events:
    date_str = event.get('date', '')
    time_str = event.get('time', '')
    timestamp = parse_standard_datetime(date_str, time_str)
    event['DateTime'] = timestamp
    if timestamp:
        permitted_converted += 1

with open('event_data_normalized/permitted_events_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(permitted_events, f, indent=4, ensure_ascii=False)

print(f"✅ Permitted: {permitted_converted}/{len(permitted_events)} events with DateTime")


# Copy Meetup events (already in correct format)
print("\nCopying Meetup events (already normalized)...")
with open('event_data_latlng/meetup_events_latlng.json', 'r', encoding='utf-8') as f:
    meetup_events = json.load(f)

with open('event_data_normalized/meetup_events_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(meetup_events, f, indent=4, ensure_ascii=False)

print(f"✅ Meetup: {len(meetup_events)} events copied")

print("\n" + "="*60)
print("✅ All events normalized and saved to event_data_normalized/")
print("="*60)
