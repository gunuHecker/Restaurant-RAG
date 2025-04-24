from bs4 import BeautifulSoup

def extract_menus_section(input_path="data/raw/pastaria_stlouis/html/Page.html", output_path="data/raw/pastaria_stlouis/html/menu.html"):
    try:
        # Read the previously saved HTML
        with open(input_path, "r", encoding="utf-8") as f:
            full_html = f.read()

        # Parse the HTML
        soup = BeautifulSoup(full_html, "html.parser")

        # Find the section with id="menus"
        menu_section = soup.find("section", id="menus")

        if menu_section:
            # Save just that section to output_path
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(str(menu_section))
            print(f"[✓] Menu section saved to {output_path}")
        else:
            print("[✗] Section with id='menus' not found.")

    except Exception as e:
        print(f"[✗] Error: {e}")

if __name__ == "__main__":
    extract_menus_section()
