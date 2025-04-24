import os
import json
from bs4 import BeautifulSoup

def extract_menu_items_from_tab_panes(input_dir="data/raw/aryabhavan/html/menu", output_file="data/raw/aryabhavan/json/menu_items.json"):
    all_items = []

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.startswith("tab_pane_") and filename.endswith(".html"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

                # Category comes from the id of the outer container div
                category_div = soup.find("div", class_="container tab-pane")
                if not category_div:
                    category_div = soup.find("div", class_="container tab-pane active")
                if not category_div:
                    continue  # Skip if not found

                category = category_div.get("id", "").strip()

                for inner_box in category_div.select("div.inner-box"):
                    name_tag = inner_box.select_one("h3.post-title.pull-left a")
                    price_tag = inner_box.select_one("h3.price.pull-right")
                    recommended_tag = inner_box.select_one("span.menu-tag")

                    # Check if recommended is truly marked
                    recommended = (
                        recommended_tag is not None and
                        "recommended" in recommended_tag.get_text(strip=True).lower()
                    )

                    if name_tag and price_tag:
                        item = {
                            "name": name_tag.text.strip(),
                            "price": price_tag.text.strip().replace("₹", "").strip(),
                            "category": category,
                            "recommended": recommended
                        }
                        all_items.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=4, ensure_ascii=False)

    print(f"[✓] Extracted {len(all_items)} items and saved to {output_file}")

if __name__ == "__main__":
    extract_menu_items_from_tab_panes()
