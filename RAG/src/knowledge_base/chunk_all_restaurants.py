import json
import os
import re

def split_text(text, max_length=512):
    # Split by sentences, then join them into chunks of max_length
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) < max_length:
            current += (" " if current else "") + sent
        else:
            if current:
                chunks.append(current)
            current = sent
    if current:
        chunks.append(current)
    return chunks

def chunk_dataset(input_path, output_path, fields_to_chunk=["description", "about_us", "our_story"], max_length=512):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    chunked_data = []
    for record in data:
        chunked = False
        for field in fields_to_chunk:
            if field in record and isinstance(record[field], str) and len(record[field]) > max_length:
                chunks = split_text(record[field], max_length)
                for i, chunk in enumerate(chunks):
                    new_record = record.copy()
                    new_record[field] = chunk
                    new_record["chunk_id"] = i
                    chunked_data.append(new_record)
                chunked = True
                break
        if not chunked:
            record["chunk_id"] = 0
            chunked_data.append(record)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunked_data, f, indent=2, ensure_ascii=False)
    print(f"Chunked data written to {output_path}")

if __name__ == "__main__":
    chunk_dataset(
        input_path="data/processed/all_restaurants.json",
        output_path="data/processed/all_restaurants_chunked.json"
    )