from bs4 import BeautifulSoup

def extract_sections(input_file="data/raw/aryabhavan/html/AboutUsPage.html", output_file="data/raw/aryabhavan/html/aboutus_sections.html"):
    # Load the saved HTML
    with open(input_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all sections with data-element_type="section"
    sections = soup.find_all("section", {"data-element_type": "section"})

    # Build a new HTML structure with just these sections
    extracted_html = "<html><head><meta charset='utf-8'></head><body>\n"
    for section in sections:
        extracted_html += str(section) + "\n"
    extracted_html += "</body></html>"

    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted_html)

    print(f"[✓] Extracted sections saved to {output_file}")

if __name__ == "__main__":
    extract_sections()