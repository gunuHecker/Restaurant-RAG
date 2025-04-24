from bs4 import BeautifulSoup
import json
import os

# Load the HTML file
with open("data/raw/CopperChimney/html/locationsPage.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Find all divs with class 'text1'
location_divs = soup.find_all("div", class_="text1")

locations = []

for div in location_divs:
    name_tag = div.find("h3")
    address_tag = div.find("p")

    if name_tag and address_tag:
        name = name_tag.get_text(strip=True)
        address = address_tag.get_text(strip=True)

        locations.append({
            "name": name,
            "address": address
        })

output_path = "data/raw/CopperChimney/json/locations.json"

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(locations, f, indent=4, ensure_ascii=False)

print(f"[✓] Saved locations to {output_path}")
