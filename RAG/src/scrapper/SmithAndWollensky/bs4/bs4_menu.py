from bs4 import BeautifulSoup
import json

def extract_menu_data(input_html="data/raw/SmithAndWollensky/menu.html", output_json="data/raw/SmithAndWollensky/menu.json"):
    with open(input_html, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    menu_data = []
    sections = soup.find_all("div", class_="yext-menu-section")

    for section in sections:
        section_title_tag = section.find("h1", class_="yext-menu-section-title")
        section_title = section_title_tag.get_text(strip=True) if section_title_tag else "Unknown Section"

        section_items = section.find_all("li", class_="yext-menu-item-details")
        for item in section_items:
            item_name = item.find("span", class_="yext-menu-item-name")
            item_price = item.find("div", class_="yext-menu-item-simple-price")
            item_desc = item.find("div", class_="yext-menu-item-desc")

            menu_item = {
                "section": section_title,
                "name": item_name.get_text(strip=True) if item_name else "",
                "price": item_price.get_text(strip=True) if item_price else "",
                "description": item_desc.get_text(strip=True) if item_desc else "",
                "options": []
            }

            options = item.find_all("div", class_="yext-menu-item-option")
            for opt in options:
                opt_text = opt.find("span", class_="yext-menu-item-option-text")
                opt_price = opt.find("div", class_="yext-menu-item-simple-price")
                menu_item["options"].append({
                    "text": opt_text.get_text(strip=True) if opt_text else "",
                    "price": opt_price.get_text(strip=True) if opt_price else ""
                })

            menu_data.append(menu_item)

    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    # Write to JSON
    with open(output_json, "w", encoding="utf-8") as out_file:
        json.dump(menu_data, out_file, indent=2, ensure_ascii=False)

    print(f"[✓] Menu data saved to {output_json}")

if __name__ == "__main__":
    extract_menu_data()
