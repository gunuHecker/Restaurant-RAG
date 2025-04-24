from bs4 import BeautifulSoup
import json
import os

def extract_location_cards(input_path="data/raw/saffron/html/locationsPage.html",
                           output_path="data/raw/saffron/json/locations.json"):
    with open(input_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find all location cards
    location_cards = soup.find_all("div", class_="bg-white h-100 hstack")

    # Extract cleaned text from each card
    locations = []
    for card in location_cards:
        text = card.get_text(separator="\n", strip=True)
        locations.append({"raw_text": text})

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save as JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(locations, f, indent=4, ensure_ascii=False)

    print(f"[✓] Saved {len(locations)} location cards to {output_path}")

if __name__ == "__main__":
    extract_location_cards()
