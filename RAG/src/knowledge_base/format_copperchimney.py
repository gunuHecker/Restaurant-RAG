import os
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'CopperChimney')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_PATH = os.path.join(PROCESSED_DIR, 'CopperChimney.json')

def load_json(filename):
    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    output = []
    # About
    about_file = 'about.json'
    if os.path.exists(os.path.join(RAW_DIR, about_file)):
        about_data = load_json(about_file)
        output.append({
            "restaurant_name": "Copper Chimney",
            "type": "about",
            "about_us": about_data.get("ABOUT US", ""),
            "our_story": about_data.get("OUR STORY", ""),
            "awards": about_data.get("AWARDS & RECOGNITIONS", ""),
            "contact": about_data.get("contact", "")
        })
    # Locations
    locations_file = 'locations.json'
    if os.path.exists(os.path.join(RAW_DIR, locations_file)):
        locations_data = load_json(locations_file)
        output.append({
            "restaurant_name": "Copper Chimney",
            "type": "location",
            "locations": locations_data
        })
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    # Ensure processed directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    # Save output
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"CopperChimney.json written to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
