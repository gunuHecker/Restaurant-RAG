# Zomato Nugget Assignment Documentation

## Project Overview
This project implements a Restaurant Retrieval-Augmented Generation (RAG) chatbot that scrapes restaurant data, processes it into a unified knowledge base, and serves it via a Streamlit UI backed by LangChain and Hugging Face.

## Tech Stack
- Python 3.8+
- Web scraping: Selenium + BeautifulSoup
- Data processing: built-in Python, JSON
- Vector DB: FAISS
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- RAG framework: LangChain + HuggingFace models
- UI: Streamlit

## Directory Structure
```
├── data/
│   ├── raw/
│   │   └── <restaurant_name>/
│   │       ├── html/          # Raw HTML pages
│   │       └── json/          # Extracted JSON
│   └── processed/
│       ├── json/              # Combined JSON per restaurant
│       └── text/              # Text files per restaurant
├── RAG/
│   ├── src/
│   │   ├── scrapper/          # Selenium + BS4 scrapers per restaurant
│   │   ├── process_data/      # Scripts to combine and normalize JSON
│   │   ├── json_to_txt/       # Generate per-restaurant text and combine
│   │   ├── knowledge_base/    # Final combined text (`combined_restaurants.txt`)
│   │   └── app/
│   │       └── streamlit_app.py  # Streamlit chatbot UI
├── requirements.txt
└── Documentation.md
```

## 1. Data Collection (Scraping)
Under `RAG/src/scrapper/`, each restaurant has a folder:
1. **Selenium scraper**: visits the live site, saves full HTML to `data/raw/<restaurant>/html/`.
2. **BS4 parser**: reads saved HTML, extracts relevant fields (about, menu, reviews, etc.), writes JSON to `data/raw/<restaurant>/json/`.

To run scraping for a restaurant:
```bash
python RAG/src/scrapper/<restaurant>/selenium_scraper.py
python RAG/src/scrapper/<restaurant>/bs4_parser.py
```

## 2. Data Processing
Scripts in `RAG/src/process_data/`:
- **process_<restaurant>.py**: combines JSON files in `data/raw/<restaurant>/json/` into one JSON.
- **combine_all_restaurants.py**: merges all processed restaurant JSONs into a single `all_restaurants.json` under `data/processed/json/`.
- Uniform structure ensures every entry has common keys: `restaurant_name`, `type`, and content fields.

Run:
```bash
python RAG/src/process_data/process_aryabhavan.py
... (others)
python RAG/src/process_data/combine_all_restaurants.py
```

## 3. Text Conversion
In `RAG/src/json_to_txt/`:
1. **generate_aryabhavan.py**: reads `Aryabhavan.json` → writes `Aryabhavan.txt` in `data/processed/text/`.
2. **generate_combine_texts.py**: loads all `.txt`, concatenates them with headers, writes `combined_restaurants.txt` into `RAG/src/knowledge_base/`.

Run:
```bash
python RAG/src/json_to_txt/generate_combine_texts.py
```

## 4. Knowledge Base
- Final knowledge file: `RAG/src/knowledge_base/combined_restaurants.txt`.
- Contains plain-text blocks separated by `# <filename>` headers.

## 5. Chatbot UI
`RAG/src/app/streamlit_app.py` implements a RAG pipeline:
1. **Loading & Splitting**: uses `TextLoader` and `RecursiveCharacterTextSplitter` to chunk `combined_restaurants.txt`.
2. **Embeddings & Vectorstore**: `HuggingFaceEmbeddings` (MiniLM) + FAISS index.
3. **Retrieval**: top-k (k=4) similarity search.
4. **LLM**: custom `HFInferenceClientLLM` via `huggingface_hub.InferenceClient` (model `Qwen/Qwen2.5-1.5B-Instruct`).
5. **Prompt Template**: instructs model to answer only from retrieved context.
6. **Pipeline**: LangChain `RunnableParallel` retrieves and formats context, passes to prompt, LLM, then parses output.
7. **Streamlit**: renders input box, shows spinner, displays answer.

### Running the Chatbot
1. Set environment variable:
   ```bash
   export HUGGINGFACEHUB_API_TOKEN="<your_token>"
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch Streamlit:
   ```bash
   streamlit run RAG/src/app/streamlit_app.py
   ```
4. Open the provided local URL, type questions about the restaurants, and get grounded answers.

## 6. Dependencies
See `requirements.txt` for full list. Key packages:
- selenium, webdriver-manager
- beautifulsoup4
- pandas, tqdm, jq
- langchain (+ community extensions)
- sentence-transformers, faiss-cpu
- streamlit, openai/accelerate/bitsandbytes for LLM support

## Future Improvements
- Automate scraping with scheduling or Airflow.
- Add caching and incremental updates.
- Support more restaurants by adding new scraper modules.
- Deploy chatbot to a live web service (Heroku/Streamlit Sharing).