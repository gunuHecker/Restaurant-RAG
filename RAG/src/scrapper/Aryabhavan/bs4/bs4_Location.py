from bs4 import BeautifulSoup
import json
import os

def extract_footer_info(html_file="data/raw/aryabhavan/html/AboutUsPage.html", output_file="data/raw/aryabhavan/json/locations.json"):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    footer_info = {}

    # Extract Address
    address_section = soup.find("div", class_="footer-left-widget")
    if address_section:
        address = address_section.find("div", class_="textwidget")
        footer_info["address"] = address.get_text(separator=" ", strip=True) if address else None

    # Extract Contact Number
    contact_section = soup.find("div", class_="footer-two-widget")
    if contact_section:
        phone_tag = contact_section.find("a", href=lambda x: x and x.startswith("tel:"))
        footer_info["contact_number"] = phone_tag.get_text(strip=True) if phone_tag else None

    # Extract Opening Hours
    hours_section = soup.find("div", class_="footer-three-widget")
    if hours_section:
        hours = hours_section.find("div", class_="textwidget")
        footer_info["opening_hours"] = hours.get_text(separator=" ", strip=True) if hours else None

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(footer_info, f, indent=2, ensure_ascii=False)

    print(f"[✓] Footer info saved to {output_file}")

if __name__ == "__main__":
    extract_footer_info()
