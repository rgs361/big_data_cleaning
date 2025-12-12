import json
import os
from add_parent_categories import CATEGORY_MAPPING

# Load Eventbrite data
with open('event_data_normalized/eventbrite_events_normalized.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

unique_categories = set()
for event in events:
    cats = event.get('Categories', [])
    if isinstance(cats, list):
        for cat in cats:
            unique_categories.add(cat)
    elif isinstance(cats, str):
        unique_categories.add(cats)

print(f"Total unique categories: {len(unique_categories)}")

unmapped = []
for cat in unique_categories:
    if cat not in CATEGORY_MAPPING:
        unmapped.append(cat)

print(f"Unmapped categories: {len(unmapped)}")
print("First 50 unmapped categories:")
for cat in sorted(unmapped)[:50]:
    print(cat)
