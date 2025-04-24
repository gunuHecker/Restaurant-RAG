import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'aryabhavan', 'json')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed', 'json')
OUTPUT_PATH = os.path.join(PROCESSED_DIR, 'Aryabhavan.json')

def load_json(filename):
    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    output = []
    # About
    about_file = 'about_us.json'
    if os.path.exists(os.path.join(RAW_DIR, about_file)):
        about_data = load_json(about_file)
        output.append({
            "restaurant_name": "Aryabhavan",
            "type": "about",
            "title": about_data.get("title", ""),
            "description": about_data.get("description", "")
        })
    # Location
    locations_file = 'locations.json'
    if os.path.exists(os.path.join(RAW_DIR, locations_file)):
        loc_data = load_json(locations_file)
        output.append({
            "restaurant_name": "Aryabhavan",
            "type": "location",
            "address": loc_data.get("address", ""),
            "contact_number": loc_data.get("contact_number", ""),
            "opening_hours": loc_data.get("opening_hours", "")
        })
    # Menu items
    menu_file = 'menu_items.json'
    if os.path.exists(os.path.join(RAW_DIR, menu_file)):
        menu_items = load_json(menu_file)
        for item in menu_items:
            output.append({
                "restaurant_name": "Aryabhavan",
                "type": "menu_item",
                "item_name": item.get("name", ""),
                "category": item.get("category", ""),
                "price": item.get("price", ""),
                "recommended": item.get("recommended", False)
            })
    # Reviews
    reviews_file = 'reviews.json'
    if os.path.exists(os.path.join(RAW_DIR, reviews_file)):
        reviews = load_json(reviews_file)
        for review in reviews:
            output.append({
                "restaurant_name": "Aryabhavan",
                "type": "review",
                "author": review.get("author", ""),
                "review": review.get("review", "")
            })
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Aryabhavan.json written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
