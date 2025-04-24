from bs4 import BeautifulSoup
import json
import os

def extract_reviews(input_file="data/raw/aryabhavan/aboutus_sections.html", output_file="data/raw/aryabhavan/reviews.json"):
    # Load the HTML content
    with open(input_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    reviews = []

    # Find all containers with testimonial content
    testimonial_blocks = soup.find_all("div", class_="testimonial-author-content")

    for block in testimonial_blocks:
        # Extract the review text
        text_tag = block.find("p", class_="testimonial-text")
        review_text = text_tag.get_text(strip=True).replace("", "").strip() if text_tag else ""

        # Extract the author name
        author_tag = block.find("h4", class_="author-name")
        author_name = author_tag.get_text(strip=True) if author_tag else "Anonymous"

        reviews.append({
            "author": author_name,
            "review": review_text
        })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save reviews to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    print(f"[✓] Extracted {len(reviews)} reviews and saved to {output_file}")

if __name__ == "__main__":
    extract_reviews()
