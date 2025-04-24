import os
import json
from glob import glob

def standardize_entry(entry):
    # Standardize location fields
    if entry.get('type') == 'location':
        # Combine raw_text and address
        if 'raw_text' in entry:
            entry['address_raw'] = entry.pop('raw_text')
        # Unify contact_number/phone
        if 'contact_number' in entry:
            entry['phone'] = entry.pop('contact_number')
        # Unify opening_hours/hours
        if 'opening_hours' in entry:
            entry['hours'] = entry.pop('opening_hours')
    # Standardize about fields
    if entry.get('type') == 'about':
        if 'Who we are' in entry:
            entry['about_us'] = entry.pop('Who we are')
        if 'Our Commitment' in entry:
            entry['commitment'] = entry.pop('Our Commitment')
        if 'title' in entry and 'about_us' not in entry:
            entry['about_us'] = entry.pop('title')
        if 'description' in entry and 'about_us' not in entry:
            entry['about_us'] = entry.pop('description')
    # Standardize menu item fields
    if entry.get('type') == 'menu_item':
        if 'name' in entry:
            entry['item_name'] = entry.pop('name')
        if 'ingridients' in entry:
            entry['description'] = entry.pop('ingridients')
        if 'options' not in entry:
            entry['options'] = []
    return entry

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    processed_dir = os.path.join(project_root, 'data', 'processed')
    output_path = os.path.join(processed_dir, 'all_restaurants.json')
    os.makedirs(processed_dir, exist_ok=True)
    all_entries = []
    for file in glob(os.path.join(processed_dir, '*.json')):
        if os.path.basename(file) == 'all_restaurants.json':
            continue
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
                for entry in data:
                    all_entries.append(standardize_entry(entry))
            except Exception as e:
                print(f"Error reading {file}: {e}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)
    print(f"Combined {len(all_entries)} entries into {output_path}")

if __name__ == '__main__':
    main()
