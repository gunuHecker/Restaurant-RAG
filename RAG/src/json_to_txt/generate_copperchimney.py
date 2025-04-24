import json
from pathlib import Path

# Paths
data_file   = Path("data/processed/all_restaurants.json")
output_file = Path("data/processed/text/CopperChimney.txt")

# Load all records
with open(data_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Keep only Copper Chimney entries
copper = [r for r in records if r.get("restaurant_name") == "Copper Chimney"]

lines = []
rest = "Copper Chimney"

for rec in copper:
    t = rec.get("type")
    if t == "about":
        about_u = rec.get("about_us","").strip()
        story   = rec.get("our_story","").strip()
        awards  = rec.get("awards","").strip()
        contact = rec.get("contact","").strip()

        if about_u:
            lines.append(f"{rest} about_us -- {about_u}")
        if story:
            lines.append(f"{rest} has a story that {story}")
        if awards:
            lines.append(f"{rest} has won awards including {awards}")
        if contact:
            lines.append(f"{rest} has contact information {contact}")

    elif t == "location":
        # support list under 'locations' or single 'name'/'address'
        if rec.get("locations"):
            for loc in rec["locations"]:
                name = loc.get("name", "").strip()
                address = loc.get("address", "").strip()
                if name and address:
                    lines.append(f"{rest} has a franchise in {name} at {address}")
        else:
            name = rec.get("name", "").strip()
            address = rec.get("address", "").strip()
            if name and address:
                lines.append(f"{rest} has a franchise in {name} at {address}")

# Ensure output dir exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Write out
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(lines)} lines to {output_file}")