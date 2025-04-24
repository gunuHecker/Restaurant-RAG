import json
from pathlib import Path

# Paths
data_file = Path("data/processed/all_restaurants.json")
output_file = Path("data/processed/text/Paakshala.txt")

# Load all records
with open(data_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Filter for Paakshala
paaks = [r for r in records if r.get("restaurant_name") == "Paakshala"]

lines = []
rest = "Paakshala Restaurant"

for rec in paaks:
    t = rec.get("type")
    if t == "location":
        name = rec.get("name", "").strip()
        address = rec.get("address", "").strip()
        phone = rec.get("phone", "").strip()
        if name and address:
            lines.append(f"{rest} has a franchise in {name} at {address}")
        if phone:
            lines.append(f"{rest} at {address} has contact number {phone}")
    elif t == "menu_item":
        item = rec.get("item_name", "").strip()
        cat = rec.get("category", "").strip()
        desc = rec.get("description", "").strip()
        if item:
            lines.append(f"{rest} has menu item {item} in category {cat}, description: {desc}")
        options = rec.get("options", [])
        if options:
            opts = ", ".join(options)
            lines.append(f"{rest}'s {item} options: {opts}")

# Ensure output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(lines)} lines to {output_file}")
