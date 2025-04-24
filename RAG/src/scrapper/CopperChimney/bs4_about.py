from bs4 import BeautifulSoup
import json
import os

# Load the HTML file
with open("data/raw/CopperChimney/AboutPage.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Find all container divs
containers = soup.find_all("div", class_="container")

about_data = {}

for container in containers:
    heading = container.find("h3")
    paragraphs = container.find_all("p")

    if heading and paragraphs:
        title = heading.get_text(strip=True)
        content = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        about_data[title] = content

# Save to JSON
os.makedirs("data/raw/CopperChimney", exist_ok=True)
with open("data/raw/CopperChimney/about.json", "w", encoding="utf-8") as f:
    json.dump(about_data, f, indent=4, ensure_ascii=False)

print("[✓] Saved About page content to data/raw/CopperChimney/about.json")
