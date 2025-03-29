import pandas as pd
import os as os

# Get the current working directory (this will be inside 'src')
current_dir = os.getcwd()

# Construct the relative path to the Excel file
file_path = os.path.join(current_dir, 'App_data', 'datasets', 'amazon_products_2023.xlsx')

# Load the Excel file
df = pd.read_excel(file_path)

"""
    Extract relevant data from a given DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to extract data from.
    
    Returns
    -------
    pandas.DataFrame
        A new DataFrame containing the extracted data.
    """
def extract_data(df):
    # Define the desired columns in new_data
    new_data = {
        'Title': [],
        'Brand': [],
        'Categories': [],
        'Main_Category': [],
        'Features': [],
        'Description': [],
        'Average_Rating': [],
        'Price': []
    }
    
    # Get the list of columns that exist in both df and new_data (case-insensitive)
    available_columns = [col for col in new_data.keys() if col.lower() in [c.lower() for c in df.columns]]
    
    # If no matching columns, return an empty DataFrame with the desired structure
    if not available_columns:
        print("No matching columns found in the input DataFrame.")
        return pd.DataFrame(new_data)
    
    # Extract data only for available columns
    for col in available_columns:
        # Find the actual column name in df (preserving its original case)
        actual_col = next(c for c in df.columns if c.lower() == col.lower())
        new_data[col] = df[actual_col].tolist()
    
    # Create and return the new DataFrame with only the available columns
    new_df = pd.DataFrame({col: new_data[col] for col in available_columns})
    return new_df

# Extract the data and store it in a new DataFrame
new_df = extract_data(df)

# Export to Excel
output_file_name = 'new_amazon_product_data.xlsx'
os.chdir(os.path.join(current_dir, 'App_data', 'datasets'))
new_df.to_excel(output_file_name, index=False)

print(f"Dataset with newly extracted data '{output_file_name}'")
