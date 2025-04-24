import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'SmithAndWollensky')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_PATH = os.path.join(PROCESSED_DIR, 'SmithAndWollensky.json')

def load_json(filename):
    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    output = []
    # About
    about_file = 'about.json'
    if os.path.exists(os.path.join(RAW_DIR, about_file)):
        about_data = load_json(about_file)
        about_entry = {
            "restaurant_name": "Smith & Wollensky",
            "type": "about",
        }
        about_entry.update(about_data)
        output.append(about_entry)

    locations_file = 'location.json'
    loc_path = os.path.join(RAW_DIR, locations_file)
    if os.path.exists(loc_path):
        loc_data = load_json(locations_file)
        # If it's a list, iterate; if dict, wrap in list
        if isinstance(loc_data, dict):
            loc_data = [loc_data]
        for loc in loc_data:
            output.append({
                "restaurant_name": "Smith & Wollensky",
                "type": "location",
                "name": loc.get("name", ""),
                "address": loc.get("address", ""),
                "phone": loc.get("phone", ""),
                "email": loc.get("email", ""),
                "hours": loc.get("hours", "")
            })
    # Menu items
    menu_file = 'menu.json'
    if os.path.exists(os.path.join(RAW_DIR, menu_file)):
        menu_items = load_json(menu_file)
        for item in menu_items:
            output.append({
                "restaurant_name": "Smith & Wollensky",
                "type": "menu_item",
                "item_name": item.get("name", ""),
                "category": item.get("section", ""),
                "description": item.get("description", ""),
                "price": item.get("price", ""),
                "options": item.get("options", [])
            })
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"SmithAndWollensky.json written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
