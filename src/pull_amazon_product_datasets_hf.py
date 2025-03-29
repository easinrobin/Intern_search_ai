from datasets import load_dataset
import pandas as pd

# Load the dataset from Hugging Face
dataset = load_dataset("smartcat/Amazon_Products_2023")

# Convert the 'train' split to a pandas DataFrame
df = pd.DataFrame(dataset['train'])

# Save to Excel
output_file = 'amazon_products_2023.xlsx'
df.to_excel(output_file, index=False)

print(f"Dataset has been downloaded and saved as '{output_file}'")