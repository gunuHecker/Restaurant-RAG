from bs4 import BeautifulSoup
import json

def parse_paakshala_menu(html_path="data/raw/Paakshala/html/menuPage.html", output_json_path="data/raw/Paakshala/json/menu.json"):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    menu = []
    sections = soup.find_all("div", class_="elementor-widget-container")

    current_category = None

    for section in sections:
        heading = section.find("h3", class_="elementor-heading-title")
        if heading:
            current_category = heading.get_text(strip=True)
            continue

        price_list = section.find("ul", class_="elementor-price-list")
        if price_list and current_category:
            items = price_list.find_all("li", class_="elementor-price-list-item")
            for item in items:
                name = item.find("span", class_="elementor-price-list-title").get_text(strip=True)
                desc_tag = item.find("p", class_="elementor-price-list-description")
                description = desc_tag.get_text(strip=True) if desc_tag else ""

                menu.append({
                    "category": current_category,
                    "name": name,
                    "description": description
                })

    # Save to JSON
    import os
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(menu, f, indent=2, ensure_ascii=False)

    print(f"[✓] Parsed menu saved to {output_json_path}")

if __name__ == "__main__":
    parse_paakshala_menu()
