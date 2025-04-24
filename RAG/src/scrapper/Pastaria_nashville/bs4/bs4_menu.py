from bs4 import BeautifulSoup
import json

def extract_menu_items(input_path="data/raw/pastaria_nashville/html/menu.html", output_path="data/raw/pastaria_nashville/json/menu.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    menu_data = []

    # Go through each submenu
    for submenu in soup.find_all("div", class_="submenu"):
        category_tag = submenu.find("h3")
        category = category_tag.get_text(strip=True) if category_tag else "Unknown"

        current = category_tag.find_next_sibling()
        while current:
            if current.name == "h3":
                break  # Reached next category
            if current.name == "h4":
                item_name = current.get_text(strip=True)
                price_tag = current.find("span", class_="price")
                if price_tag:
                    price_text = price_tag.get_text(strip=True)
                    item_name = item_name.replace(price_text, "").strip()
                    try:
                        # Always take first price if there's a range, and append " dollars"
                        price = f"{float(price_text.split('/')[0]):.2f} dollars"
                    except ValueError:
                        price = None
                else:
                    price = None

                # Get ingridients (usually in the next <div class="entry">)
                desc_div = current.find_next_sibling("div", class_="entry")
                ingridients = desc_div.get_text(" ", strip=True) if desc_div else ""

                menu_data.append({
                    "category": category,
                    "item": item_name,
                    "price": price,
                    "ingridients": ingridients
                })
            current = current.find_next_sibling()

    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(menu_data, f, indent=2)

    print(f"[✓] Extracted {len(menu_data)} items to {output_path}")

if __name__ == "__main__":
    extract_menu_items()
