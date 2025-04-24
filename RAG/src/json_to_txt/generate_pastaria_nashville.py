import json
from pathlib import Path

# Paths
data_file = Path("data/processed/all_restaurants.json")
output_file = Path("data/processed/text/PastariaNashville.txt")

# Load all records
with open(data_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Filter for Pastaria Nashville
pastaria = [r for r in records if r.get("restaurant_name") == "Pastaria Nashville"]

lines = []
rest = "Pastaria Nashville Restaurant"

for rec in pastaria:
    t = rec.get("type")
    if t == "location":
        addr = rec.get("address", "").strip()
        phone = rec.get("phone", "").strip()
        email = rec.get("email", "").strip()
        hours = rec.get("hours", [])
        if addr:
            lines.append(f"{rest} is situated at -- {addr}")
        if phone:
            lines.append(f"{rest} has contact number: {phone}")
        if email:
            lines.append(f"{rest} has email: {email}")
        for h in hours:
            lines.append(f"{rest} opening hours: {h}")

    elif t == "menu_item":
        name = rec.get("item_name", "").strip()
        cat = rec.get("category", "").strip()
        desc = rec.get("description", "").strip()
        price = (rec.get("price") or "").strip()
        if name:
            lines.append(f"{rest} has menu item, {name} in {cat} priced at {price}.")
            if desc:
                lines.append(f"Description: {desc}")
        options = rec.get("options", [])
        if options:
            opts = ", ".join(options)
            lines.append(f"{rest}'s {name} options: {opts}")

# Ensure output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(lines)} lines to {output_file}")
