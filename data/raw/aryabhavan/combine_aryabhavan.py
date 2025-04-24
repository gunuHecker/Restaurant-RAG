import json
import os

# Directory containing the JSON files
dir = os.path.dirname(__file__)

# Load about_us.json
with open(os.path.join(dir, 'about_us.json'), 'r', encoding='utf-8') as f:
    about_us = json.load(f)

# Load locations.json
with open(os.path.join(dir, 'locations.json'), 'r', encoding='utf-8') as f:
    location = json.load(f)

# Load menu_items.json
with open(os.path.join(dir, 'menu_items.json'), 'r', encoding='utf-8') as f:
    menu_items = json.load(f)

# Load reviews.json
with open(os.path.join(dir, 'reviews.json'), 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Compose the unified structure
combined = {
    "restaurant_name": "Arya Bhavan",
    "about": {
        "title": about_us.get("title", ""),
        "description": about_us.get("description", "")
    },
    "location": {
        "address": location.get("address", ""),
        "contact_number": location.get("contact_number", ""),
        "opening_hours": location.get("opening_hours", "")
    },
    "menu_items": menu_items,
    "reviews": reviews
}

# Output file
with open(os.path.join(dir, 'aryabhavan_combined.json'), 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print("Unified Aryabhavan data written to aryabhavan_combined.json")
