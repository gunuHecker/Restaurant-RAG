from bs4 import BeautifulSoup
import os

def extract_menu_section(input_path="data/raw/SmithAndWollensky/MenuPage.html", output_path="data/raw/SmithAndWollensky/menu.html"):
    # Load the full page HTML
    with open(input_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Extract the section containing the menu
    menu_section = soup.find("section", class_="m__menus module module__2")
    if menu_section:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(menu_section.prettify())
        print(f"[✓] Menu section extracted and saved to {output_path}")
    else:
        print("[✗] Menu section not found in the HTML.")

if __name__ == "__main__":
    extract_menu_section()
