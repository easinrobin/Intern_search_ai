from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import re

# Load model, index, and data
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("product_index.faiss")
products = pd.read_csv("processed_products.csv")

def parse_query(query):
    """Extract specific intent filters from the query."""
    filters = {}

    # Brand detection (e.g., "Amazon brand")
    brand_match = re.search(r"(amazon|[\w]+)\s+brand", query, re.IGNORECASE)
    if brand_match:
        filters["Brand"] = brand_match.group(1).capitalize()
    
    # Price detection (e.g., "under $500", "less than 200")
    price_match = re.search(r"(under|less than)\s*\$?(\d+)", query, re.IGNORECASE)
    if price_match:
        filters["Price"] = float(price_match.group(2))
    
    # Clean query for embedding (remove filter terms)
    cleaned_query = re.sub(r"(under|less than)\s*\$?\d+", "", query)
    cleaned_query = re.sub(r"[\w]+\s+brand", "", cleaned_query).strip()
    
    return cleaned_query, filters

def search_products(query, top_k=10):
    # Parse query for filters
    cleaned_query, filters = parse_query(query)
    print(f"Cleaned Query: {cleaned_query}, Filters: {filters}")  # Debugging
    
    # Convert query to embedding
    query_embedding = model.encode([cleaned_query])[0].astype('float32')
    
    # Search the index
    distances, indices = index.search(np.array([query_embedding]), top_k)
    
    # Get initial results
    results = products.iloc[indices[0]]
    
    # Apply filters
    if "Brand" in filters:
        results = results[results["Brand"] == filters["Brand"]]
    if "Price" in filters:
        results = results[results["Price"] < filters["Price"]]
    
    return results.to_dict('records')

# # Test it
# query = "Kisbaby Blanket"
# results = search_products(query)
# for r in results:
#     print(f"Name: {r['Title']}, Brand: {r['Brand']}, Price: {r['Price']}, Category: {r['Main_Category']}")