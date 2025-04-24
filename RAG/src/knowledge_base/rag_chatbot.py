import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# --- Load FAISS index and metadata ---
with open('data/processed/all_restaurants_embedded.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

embeddings = []
metadata = []
for record in data:
    if record.get('embedding') is not None:
        embeddings.append(record['embedding'])
        metadata.append(record)

embeddings = np.array(embeddings).astype('float32')
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# --- Load embedding model ---
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# --- Load LLM for answer generation (using FLAN-T5 as an example) ---
# You can swap for another model if you want
llm_model_name = "google/flan-t5-base"
llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
llm_model = AutoModelForSeq2SeqLM.from_pretrained(llm_model_name)
llm_pipe = pipeline("text2text-generation", model=llm_model, tokenizer=llm_tokenizer)

def retrieve(query, k=5):
    query_emb = embed_model.encode([query]).astype('float32')
    D, I = index.search(query_emb, k)
    results = []
    for idx in I[0]:
        results.append(metadata[idx])
    return results

def build_context(retrieved_chunks):
    # Concatenate the text_for_embedding fields for context
    return "\n".join([chunk.get("text_for_embedding", "") for chunk in retrieved_chunks])

def generate_answer(question, context):
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    result = llm_pipe(prompt, max_new_tokens=128)[0]['generated_text']
    return result.strip()

if __name__ == "__main__":
    print("Welcome to the Restaurant RAG Chatbot! (type 'exit' to quit)")
    while True:
        user_query = input("\nAsk a question: ")
        if user_query.lower() in ["exit", "quit"]:
            break
        retrieved = retrieve(user_query, k=5)
        context = build_context(retrieved)
        answer = generate_answer(user_query, context)
        print("\n--- Answer ---")
        print(answer)
        print("\n--- Top Retrieved Chunks ---")
        for i, chunk in enumerate(retrieved, 1):
            print(f"{i}. [{chunk.get('restaurant_name')}] {chunk.get('type')}: {chunk.get('text_for_embedding', '')[:200]}") 