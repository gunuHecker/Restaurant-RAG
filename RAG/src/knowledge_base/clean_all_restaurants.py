import json
import unicodedata
import re
import os

def clean_string(s):
    # Normalize unicode
    s = unicodedata.normalize('NFKC', s)
    # Remove excessive whitespace (collapse multiple spaces, tabs, newlines)
    s = re.sub(r'\s+', ' ', s)
    # Strip leading/trailing whitespace
    s = s.strip()
    # Remove non-printable characters
    s = ''.join(ch for ch in s if ch.isprintable())
    return s

def clean_record(record):
    if isinstance(record, dict):
        return {k: clean_record(v) for k, v in record.items()}
    elif isinstance(record, list):
        return [clean_record(v) for v in record]
    elif isinstance(record, str):
        return clean_string(record)
    else:
        return record

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    input_path = os.path.join(project_root, 'data', 'processed', 'all_restaurants_chunked.json')
    output_path = os.path.join(project_root, 'data', 'processed', 'all_restaurants_cleaned.json')
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cleaned_data = [clean_record(record) for record in data]
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    print(f"Cleaned data written to {output_path}")

if __name__ == '__main__':
    main()
