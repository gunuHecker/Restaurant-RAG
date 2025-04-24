from bs4 import BeautifulSoup
import json

def extract_location_info_from_html(html_path="data/raw/SmithAndWollensky/LocationPage.html", output_json_path="data/raw/SmithAndWollensky/location.json"):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Extract address
    address_block = soup.find("p", string="Address")
    if address_block:
        address_block = address_block.find_next("div")
        address_lines = [line.strip() for line in address_block.stripped_strings if "View on Google maps" not in line]
        address = " ".join(address_lines)
    else:
        address = None

    # Extract hours of operation
    hours_block = soup.find("p", string="Hours of Operation:")
    if hours_block:
        hours_block = hours_block.find_next("div")
        hours = "\n".join(line.strip() for line in hours_block.stripped_strings)
    else:
        hours = None

    # Extract phone number
    phone_block = soup.find("p", string="PHONE")
    if phone_block:
        phone_block = phone_block.find_next("div")
        phone = phone_block.a.text.strip() if phone_block and phone_block.a else None
    else:
        phone = None

    # Extract email
    email_block = soup.find("p", string="EMAIL")
    if email_block:
        email_block = email_block.find_next("div")
        email = email_block.a.text.strip() if email_block and email_block.a else None
    else:
        email = None

    # Combine everything into a dictionary
    location_data = {
        "name": "Smith & Wollensky - Boston",
        "address": address,
        "hours": hours,
        "phone": phone,
        "email": email
    }

    # Ensure the output directory exists
    import os
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Write to JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(location_data, f, indent=4)

    print(f"[✓] Location information saved to {output_json_path}")

if __name__ == "__main__":
    extract_location_info_from_html()
