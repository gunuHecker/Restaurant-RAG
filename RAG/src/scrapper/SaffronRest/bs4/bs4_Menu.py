from bs4 import BeautifulSoup
import json

# Load the HTML from a file
with open("data/raw/saffron/menuPage.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# Step 1: Get all tab panes that contain menu items
tab_panes = soup.select(".tab-content .tab-pane")

menu_data = []

for pane in tab_panes:
    category_id = pane.get("id")  # e.g., "appetizers", "soup"
    category_name_tag = soup.select_one(f'a[data-bs-target="#{category_id}"]')
    category_name = category_name_tag.text.strip() if category_name_tag else "Unknown Category"

    for li in pane.select("ul > li"):
        item_name_tag = li.find("span", class_="fw-bold")
        item_description_tag = li.find_all("span", class_="name")
        
        item_name = item_name_tag.get_text(strip=True) if item_name_tag else "Unnamed Item"
        item_description = item_description_tag[1].get_text(strip=True) if len(item_description_tag) > 1 else ""

        menu_data.append({
            "category": category_name,
            "item_name": item_name,
            "description": item_description
        })

# Save to JSON
with open("data/raw/saffron/menu.json", "w", encoding="utf-8") as json_file:
    json.dump(menu_data, json_file, ensure_ascii=False, indent=2)

print("Scraped menu saved to data/raw/saffron/menu.json")
