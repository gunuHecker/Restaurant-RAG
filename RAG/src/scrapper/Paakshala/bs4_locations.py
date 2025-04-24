from bs4 import BeautifulSoup
import json
import os

def extract_locations_from_html(input_path="data/raw/Paakshala/locationsPage.html", output_path="data/raw/Paakshala/locations.json"):
    # Load your HTML content (as string)
    with open(input_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    locations = []

    # Find all heading blocks that contain the branch name
    heading_blocks = soup.find_all("div", class_="elementor-widget-heading")

    for heading_block in heading_blocks:
        name_tag = heading_block.find("h2", class_="elementor-heading-title")
        if not name_tag or not name_tag.a:
            continue

        name = name_tag.get_text(strip=True)
        parent = heading_block.find_parent("div", class_="elementor-element")

        # Look ahead in the sibling divs for address and phone
        address_tag = parent.find_next("div", class_="elementor-widget-text-editor")
        phone_tag = parent.find_next("a", href=lambda href: href and href.startswith("tel:"))

        address = address_tag.get_text(strip=True) if address_tag else ""
        phone = phone_tag.get_text(strip=True) if phone_tag else ""

        locations.append({
            "name": name,
            "address": address,
            "phone": phone
        })

    # Output the result to console
    print(json.dumps(locations, indent=2, ensure_ascii=False))

    # Also save it to a JSON file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(locations, out_file, indent=2, ensure_ascii=False)

    print(f"[✓] Extracted {len(locations)} locations to {output_path}")


if __name__ == "__main__":
    extract_locations_from_html()
