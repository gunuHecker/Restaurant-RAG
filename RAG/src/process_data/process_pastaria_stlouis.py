import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'pastaria_stlouis', 'json')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed', 'json')
OUTPUT_PATH = os.path.join(PROCESSED_DIR, 'PastariaStLouis.json')

def load_json(filename):
    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    output = []
    # Location
    location_file = 'location.json'
    if os.path.exists(os.path.join(RAW_DIR, location_file)):
        loc_data = load_json(location_file)
        output.append({
            "restaurant_name": "Pastaria St. Louis",
            "type": "location",
            "address": loc_data.get("address", ""),
            "phone": loc_data.get("phone", ""),
            "email": loc_data.get("email", ""),
            "hours": loc_data.get("hours", [])
        })
    # Menu items
    menu_file = 'menu.json'
    if os.path.exists(os.path.join(RAW_DIR, menu_file)):
        menu_items = load_json(menu_file)
        for item in menu_items:
            output.append({
                "restaurant_name": "Pastaria St. Louis",
                "type": "menu_item",
                "item_name": item.get("item", ""),
                "category": item.get("category", ""),
                "description": item.get("ingridients", ""),
                "price": item.get("price", "")
            })
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"PastariaStLouis.json written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
