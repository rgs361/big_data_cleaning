import json
import os

def extract_unique_categories():
    unique_categories = set()
    
    base_path = 'event_data_normalized'
    
    files_config = [
        {
            'filename': 'eventbrite_events_normalized.json',
            'field': 'category',
            'is_list': False
        },
        {
            'filename': 'meetup_events_normalized.json',
            'field': 'Categories',
            'is_list': True
        },
        {
            'filename': 'nyc_park_events_normalized.json',
            'field': 'category',
            'is_list': False
        },
        {
            'filename': 'permitted_events_normalized.json',
            'field': 'category',
            'is_list': False
        }
    ]
    
    for config in files_config:
        file_path = os.path.join(base_path, config['filename'])
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found.")
            continue
            
        print(f"Processing {config['filename']}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for item in data:
                    field_name = config['field']
                    if field_name in item:
                        value = item[field_name]
                        
                        if config['is_list']:
                            if isinstance(value, list):
                                for cat in value:
                                    if cat:
                                        unique_categories.add(cat.strip())
                        else:
                            if value:
                                unique_categories.add(value.strip())
                                
        except Exception as e:
            print(f"Error processing {config['filename']}: {e}")

    # Sort categories alphabetically
    sorted_categories = sorted(list(unique_categories))
    
    output_file = 'unique_categories.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for category in sorted_categories:
            f.write(f"{category}\n")
            
    print(f"Successfully wrote {len(sorted_categories)} unique categories to {output_file}")

if __name__ == "__main__":
    extract_unique_categories()
