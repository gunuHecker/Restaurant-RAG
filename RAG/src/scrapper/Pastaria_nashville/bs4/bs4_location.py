from bs4 import BeautifulSoup
import json

def extract_location_data(input_path="data/raw/pastaria_nashville/html/Page.html", output_path="data/raw/pastaria_nashville/json/location.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Extract address
    address_tag = soup.select_one("header address a")
    address = address_tag.get_text(strip=True) if address_tag else None

    # Extract phone number
    phone_tag = soup.select_one("div.phone span")
    phone = phone_tag.get_text(strip=True) if phone_tag else None

    # Extract email
    email_tag = soup.select_one("div.phone a[href^='mailto']")
    email = email_tag["href"].replace("mailto:", "") if email_tag else None

    # Extract hours
    hours_section = soup.find("section", id="hours")
    hours = []
    if hours_section:
        rows = hours_section.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 1:
                text = cols[0].get_text(strip=True)
                if text:
                    hours.append(text)
            elif len(cols) >= 2:
                text = cols[0].get_text(strip=True)
                if text:
                    hours.append(text)

    location_data = {
        "address": address,
        "phone": phone,
        "email": email,
        "hours": hours
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(location_data, f, indent=2)

    print(f"[✓] Location data extracted and saved to {output_path}")

if __name__ == "__main__":
    extract_location_data()
