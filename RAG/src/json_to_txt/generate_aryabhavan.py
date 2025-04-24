import json
from pathlib import Path

# Paths
data_file = Path("data/processed/all_restaurants.json")
output_file = Path("data/processed/text/aryabhavan.txt")

# Load all restaurants
with open(data_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Filter for Aryabhavan
aryas = [r for r in records if r.get("restaurant_name") == "Aryabhavan"]

lines = []
restaurant = "Aryabhavan Restaurant"

for rec in aryas:
    t = rec.get("type")
    if t == "about":
        desc    = rec.get("description", "").strip()
        about_u = rec.get("about_us", "").strip()
        if desc:
            lines.append(f"{restaurant} has description -- {desc}")
        if about_u:
            lines.append(f"{restaurant} has about us -- {about_u}")

    elif t == "location":
        addr  = rec.get("address", "").strip()
        phone = rec.get("phone", "").strip()
        hours = rec.get("hours", "").strip()
        if addr:
            lines.append(f"{restaurant} is situated at -- {addr}")
        if phone:
            lines.append(f"{restaurant} has contact number: {phone}")
        if hours:
            lines.append(f"{restaurant} is open at \"{hours}\"")

    elif t == "menu_item":
        name = rec.get("item_name", "").strip()
        cat  = rec.get("category", "").strip()
        price = rec.get("price", "").strip()
        recmd = rec.get("recommended", False)
        lines.append(
            f"{restaurant} has menu item, {name} in {cat} priced at {price} rupees."
        )
        if recmd:
            lines.append(f"{name} is recommended menu item of {restaurant}.")

# Ensure output dir exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Write to saffron.txt
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(lines)} lines to {output_file}")