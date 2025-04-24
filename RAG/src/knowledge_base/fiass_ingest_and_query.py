import json
import numpy as np
import faiss

# Load your embedded data
with open('data/processed/all_restaurants_embedded.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract embeddings and metadata
embeddings = []
metadata = []
for record in data:
    if record.get('embedding') is not None:
        embeddings.append(record['embedding'])
        metadata.append(record)  # You can store the whole record or just key fields

embeddings = np.array(embeddings).astype('float32')
dimension = embeddings.shape[1]

# Build the FAISS index (using GPU if available)
try:
    import faiss.contrib.torch_utils  # This will enable GPU
    res = faiss.StandardGpuResources()
    index = faiss.IndexFlatL2(dimension)
    gpu_index = faiss.index_cpu_to_gpu(res, 0, index)
    gpu_index.add(embeddings)
    index = gpu_index
    print("Using GPU for FAISS")
except Exception as e:
    print("Falling back to CPU for FAISS:", e)
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

print(f"FAISS index built with {index.ntotal} vectors.")

# --- Test retrieval ---

def search(query_text, model, k=5):
    # Get embedding for query
    query_emb = model.encode([query_text]).astype('float32')
    D, I = index.search(query_emb, k)
    results = []
    for idx in I[0]:
        results.append(metadata[idx])
    return results

# Example usage:
if __name__ == "__main__":
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Try a few sample queries
    for query in [
        "What are the hours for Aryabhavan?",
        "Tell me about Margherita Pizza",
        "Where is Saffron located?",
        "What soups are available at Copper Chimney?",
        "Who is the founder of Smith & Wollensky?"
    ]:
        print(f"\nQuery: {query}")
        results = search(query, model, k=3)
        for i, r in enumerate(results, 1):
            print(f"Result {i}:")
            print("  Restaurant:", r.get("restaurant_name"))
            print("  Type:", r.get("type"))
            print("  Text:", r.get("text_for_embedding", "")[:200])