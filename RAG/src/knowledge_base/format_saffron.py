import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'saffron')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_PATH = os.path.join(PROCESSED_DIR, 'Saffron.json')

def load_json(filename):
    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    output = []
    # About
    about_file = 'about_us.json'
    if os.path.exists(os.path.join(RAW_DIR, about_file)):
        about_data = load_json(about_file)
        about_entry = {
            "restaurant_name": "Saffron",
            "type": "about",
        }
        about_entry.update(about_data)
        output.append(about_entry)
    # Locations
    locations_file = 'locations.json'
    if os.path.exists(os.path.join(RAW_DIR, locations_file)):
        locations_data = load_json(locations_file)
        for loc in locations_data:
            output.append({
                "restaurant_name": "Saffron",
                "type": "location",
                "raw_text": loc.get("raw_text", "")
            })
    # Menu items
    menu_file = 'menu.json'
    if os.path.exists(os.path.join(RAW_DIR, menu_file)):
        menu_items = load_json(menu_file)
        for item in menu_items:
            output.append({
                "restaurant_name": "Saffron",
                "type": "menu_item",
                "item_name": item.get("item_name", ""),
                "category": item.get("category", ""),
                "description": item.get("description", "")
            })
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Saffron.json written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
