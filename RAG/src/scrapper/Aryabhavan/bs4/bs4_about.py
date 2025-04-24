from bs4 import BeautifulSoup
import json

# Read the HTML file
with open('data/raw/aryabhavan/html/aboutus_sections.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title and description
title = soup.select_one('.elementor-element-19da7dd p').text.strip()
description = soup.select_one('.elementor-element-a63b6fe p').text.strip()

# Create dictionary with the extracted information
about_data = {
    "title": title,
    "description": description
}

# Save to JSON file
output_path = 'data/raw/aryabhavan/json/about_us.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(about_data, json_file, indent=4, ensure_ascii=False)

print(f"About us information has been saved to {output_path}")
