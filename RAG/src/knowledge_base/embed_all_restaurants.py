import json
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def get_text_for_embedding(record):
    t = record.get("type", "")
    text_parts = []
    if t == "menu_item":
        # Use item_name and description
        if "item_name" in record:
            text_parts.append(record["item_name"])
        if "description" in record:
            text_parts.append(record["description"])
        if "category" in record:
            text_parts.append(f"Category: {record['category']}")
    elif t == "about":
        # Use all about fields
        for field in ["about_us", "description", "our_story", "commitment"]:
            if field in record:
                text_parts.append(record[field])
    elif t == "location":
        # Use all location-relevant fields
        for field in ["name", "address", "address_raw", "hours", "phone", "email"]:
            if field in record:
                text_parts.append(str(record[field]))
    else:
        # Fallback: concatenate all string fields
        for v in record.values():
            if isinstance(v, str):
                text_parts.append(v)
    return " | ".join(text_parts)

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    input_path = os.path.join(project_root, 'data', 'processed', 'all_restaurants_cleaned.json')
    output_path = os.path.join(project_root, 'data', 'processed', 'all_restaurants_embedded.json')

    # Load model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Load data
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    embedded_data = []
    for record in tqdm(data, desc="Embedding records"):
        text = get_text_for_embedding(record)
        record["text_for_embedding"] = text
        if text.strip():
            embedding = model.encode(text).tolist()
            record['embedding'] = embedding
        else:
            record['embedding'] = None
        embedded_data.append(record)

    # Save output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(embedded_data, f, indent=2, ensure_ascii=False)
    print(f"Embeddings written to {output_path}")

if __name__ == '__main__':
    main()