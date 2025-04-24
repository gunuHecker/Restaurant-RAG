import json
from pathlib import Path

# Paths
data_file = Path("data/processed/all_restaurants.json")
output_file = Path("data/processed/text/SmithAndWollensky.txt")

# Load all records
with open(data_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Filter for Smith & Wollensky
sw = [r for r in records if r.get("restaurant_name") == "Smith & Wollensky"]

lines = []
rest = "Smith & Wollensky Restaurant"

# Location entries
for rec in sw:
    if rec.get("type") == "location":
        name = (rec.get("name") or "").strip()
        address = (rec.get("address") or "").strip()
        phone = (rec.get("phone") or "").strip()
        email = (rec.get("email") or "").strip()
        hours_raw = rec.get("hours") or ""
        if name and address:
            lines.append(f"{rest} has location {name} at {address}")
        elif address:
            lines.append(f"{rest} is located at {address}")
        if phone:
            lines.append(f"{rest} has contact number: {phone}")
        if email:
            lines.append(f"{rest} has email: {email}")
        for h in hours_raw.splitlines():
            h = h.strip()
            if h:
                lines.append(f"{rest} opening hours: {h}")

# Menu items
for rec in sw:
    if rec.get("type") == "menu_item":
        item = (rec.get("item_name") or "").strip()
        cat = (rec.get("category") or "").strip()
        desc = (rec.get("description") or "").strip()
        price = (rec.get("price") or "").strip()
        if item:
            lines.append(f"{rest} has menu item {item} in category {cat} priced at {price}.")
            if desc:
                lines.append(f"{item} description: {desc}")
        options = rec.get("options") or []
        for opt in options:
            text = (opt.get("text") or "").strip()
            pr = (opt.get("price") or "").strip()
            if text and pr:
                lines.append(f"{rest}'s {item} add-on {text} at {pr}")

# Ensure output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(lines)} lines to {output_file}")
