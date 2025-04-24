import json
from pathlib import Path

# Paths
data_file = Path("data/processed/all_restaurants.json")
output_file = Path("data/processed/text/Saffron.txt")

# Load all records
with open(data_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Filter for Saffron entries
saffron = [r for r in records if r.get("restaurant_name") == "Saffron"]
lines = []
rest = "Saffron Restaurant"

# About section
abouts = [r for r in saffron if r.get("type") == "about"]
if abouts:
    about = abouts[0]
    for award in about.get("Awards", []):
        title = award.get("title", "").strip()
        year = award.get("year", "").strip()
        if title or year:
            lines.append(f"{rest} award: {title} ({year})")
    vision = (about.get("Vision") or "").strip()
    if vision:
        lines.append(f"{rest} vision: {vision}")
    mission = (about.get("Mission") or "").strip()
    if mission:
        lines.append(f"{rest} mission: {mission}")
    about_us = (about.get("about_us") or "").strip()
    if about_us:
        lines.append(f"{rest} about us: {about_us}")
    commitment = (about.get("commitment") or "").strip()
    if commitment:
        lines.append(f"{rest} commitment: {commitment}")

# Location entries
for rec in saffron:
    if rec.get("type") == "location":
        raw = (rec.get("address_raw") or "").strip()
        if raw:
            flat = " | ".join(line.strip() for line in raw.splitlines() if line.strip())
            lines.append(f"{rest} location: {flat}")

# Menu items
for rec in saffron:
    if rec.get("type") == "menu_item":
        item = (rec.get("item_name") or "").strip()
        cat = (rec.get("category") or "").strip()
        desc = (rec.get("description") or "").strip()
        if item:
            lines.append(f"{rest} menu item: {item} | category: {cat} | description: {desc}")
        options = rec.get("options") or []
        if options:
            lines.append(f"{rest} {item} options: {', '.join(options)}")

# Write out
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(lines)} lines to {output_file}")
