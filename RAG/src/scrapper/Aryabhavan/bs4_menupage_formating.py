from bs4 import BeautifulSoup
import os

def extract_tab_pane_divs(html_path="data/raw/aryabhavan/menuPage.html"):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all divs where class contains 'container' and 'tab-pane'
    tab_pane_divs = soup.find_all("div", class_=lambda x: x and "container" in x and "tab-pane" in x)

    print(f"[✓] Found {len(tab_pane_divs)} relevant divs")

    # Optional: return all the inner HTMLs as strings
    extracted_contents = [str(div) for div in tab_pane_divs]

    return extracted_contents

if __name__ == "__main__":
    tab_panes = extract_tab_pane_divs()
    output_dir = "data/raw/aryabhavan/menu"
    os.makedirs(output_dir, exist_ok=True)

    for i, content in enumerate(tab_panes):
        with open(f"{output_dir}/tab_pane_{i+1}.html", "w", encoding="utf-8") as f:
            f.write(content)