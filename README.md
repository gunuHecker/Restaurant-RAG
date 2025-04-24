# Zomato Nugget Assignment

A Retrieval-Augmented Generation (RAG) chatbot for restaurant data scraped from various Zomato pages. It automates data collection, processing, text conversion, and serves a Streamlit-based interactive UI using LangChain and Hugging Face.

## Features
- Web scraping via Selenium + BeautifulSoup
- JSON extraction and normalization per restaurant
- Combined knowledge base creation
- Embedding vectorstore with FAISS
- LangChain RAG pipeline with Hugging Face models
- Streamlit UI for interactive Q&A

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd "Zomato Nugget Assignment"
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure
```
Zomato Nugget Assignment/
├── data/
│   ├── raw/                  # HTML & JSON from scrapers
│   └── processed/            # Combined JSON & text files
├── RAG/
│   └── src/
│       ├── scrapper/         # Selenium + BS4 per-restaurant
│       ├── process_data/     # Combine & normalize JSONs
│       ├── json_to_txt/      # Generate text & combine into KB
│       ├── knowledge_base/   # Final combined_restaurants.txt
│       └── app/
│           └── streamlit_app.py  # Streamlit RAG chatbot
├── requirements.txt
└── README.md
```

## Usage

### 1. Scrape Data

For each restaurant folder under `RAG/src/scrapper/`:
```bash
python RAG/src/scrapper/<restaurant>/selenium_scraper.py
python RAG/src/scrapper/<restaurant>/bs4_parser.py
```

### 2. Process Data

Combine JSONs and normalize:
```bash
python RAG/src/process_data/process_aryabhavan.py
# ... other restaurants
python RAG/src/process_data/combine_all_restaurants.py
```

### 3. Generate Text & Knowledge Base

```bash
python RAG/src/json_to_txt/generate_combine_texts.py
```

### 4. Run the Chatbot

1. Set your Hugging Face API token:
   ```bash
   export HUGGINGFACEHUB_API_TOKEN="<your_token>"
   ```
2. Launch Streamlit:
   ```bash
   streamlit run RAG/src/app/streamlit_app.py
   ```
3. Open the displayed URL in your browser and start asking questions.

## Contributing

Feel free to open issues or submit pull requests to add new restaurants, improve processing, or enhance the UI.