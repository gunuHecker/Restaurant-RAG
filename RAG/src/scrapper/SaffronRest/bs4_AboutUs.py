from bs4 import BeautifulSoup
import json

# Load the HTML file
with open("data/raw/saffron/AboutUsPage.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")
sections = soup.find_all("div", class_="page-section")

about_us_data = {}

for section in sections:
    # Our Commitment section
    title_tag = section.find("h3", class_="title")
    subtitle_tag = section.find("h4", class_="text-red")

    if title_tag and subtitle_tag:
        content = " ".join(p.get_text(strip=True) for p in section.find_all("p") if p.get_text(strip=True))
        about_us_data[title_tag.text.strip()] = content

    # Who We Are section
    elif section.find("h2", string="Who we are"):
        paragraphs = section.find_all("p")
        about_us_data["Who we are"] = " ".join(p.get_text(strip=True) for p in paragraphs)

    # Awards section
    elif section.find("h2", string="Awards"):
        awards = []
        for award in section.select(".award-content"):
            title = award.find("span", class_="title").text.strip()
            year = award.find("span", class_="year").text.strip()
            awards.append({"title": title, "year": year})
        about_us_data["Awards"] = awards

    # Vision and Mission section
    elif section.find("em", string="Vision") or section.find("em", string="Mission"):
        for block in section.select(".bg-gray"):
            label = block.find("em")
            content = block.find_all("p")[-1].get_text(strip=True)
            if label:
                about_us_data[label.text.strip()] = content

# Save to JSON
with open("data/raw/saffron/about_us.json", "w", encoding="utf-8") as f:
    json.dump(about_us_data, f, ensure_ascii=False, indent=2)

print("✅ About Us content saved to 'data/raw/saffron/about_us.json'")
