import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os as os

# Get the current working directory (this will be inside 'src')
current_dir = os.getcwd()

# Construct the relative path to the Excel file
file_path = os.path.join(current_dir, 'App_data', 'datasets', 'new_amazon_product_data.xlsx')

# Load the Excel file
data = pd.read_excel(file_path)

# Combine textual columns into a single string per product
def combine_text(row):
    return f"{row['Title']} {row['Brand']} {row['Categories']} {row['Main_Category']} {row['Features']} {row['Description']}"

data["combined_product_data"] = data.apply(combine_text, axis=1)

# Load a pre-trained embedding model (still lightweight for resource constraints)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for the combined text
embeddings = model.encode(data['combined_product_data'].tolist(), batch_size=32, show_progress_bar=True)

# Save embeddings and full dataset
np.save("product_embeddings.npy", embeddings)
data.to_csv("processed_products.csv")

# Build FAISS index
dimension = embeddings.shape[1] # e.g., 384 for MiniLM
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))
faiss.write_index(index, "product_index.faiss")

print("Dataset prepared with embeddings and vector index built!")