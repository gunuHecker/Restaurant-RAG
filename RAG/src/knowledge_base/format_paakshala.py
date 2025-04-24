import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'Paakshala')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_PATH = os.path.join(PROCESSED_DIR, 'Paakshala.json')

def load_json(filename):
    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    output = []
    # Locations
    locations_file = 'locations.json'
    if os.path.exists(os.path.join(RAW_DIR, locations_file)):
        locations_data = load_json(locations_file)
        for loc in locations_data:
            output.append({
                "restaurant_name": "Paakshala",
                "type": "location",
                "name": loc.get("name", ""),
                "address": loc.get("address", ""),
                "phone": loc.get("phone", "")
            })
    # Menu items
    menu_file = 'menu.json'
    if os.path.exists(os.path.join(RAW_DIR, menu_file)):
        menu_items = load_json(menu_file)
        for item in menu_items:
            output.append({
                "restaurant_name": "Paakshala",
                "type": "menu_item",
                "item_name": item.get("name", ""),
                "category": item.get("category", ""),
                "description": item.get("description", "")
            })
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Paakshala.json written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
