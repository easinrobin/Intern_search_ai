import pandas as pd
from openpyxl import load_workbook
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path.cwd()
INPUT_FILE = BASE_DIR / 'App_data' / 'datasets' / 'amazon_products_2023.xlsx'
OUTPUT_FILE = BASE_DIR / 'App_data' / 'datasets' / 'new_amazon_product_data.xlsx'
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def extract_data(chunk):
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
    
    available_columns = set(new_data.keys()).intersection(set(col.lower() for col in chunk.columns))
    available_columns = [col for col in new_data.keys() if col.lower() in available_columns]
    
    if not available_columns:
        logger.warning("No matching columns found in this chunk.")
        return pd.DataFrame(new_data)
    
    new_df = chunk[[next(c for c in chunk.columns if c.lower() == col.lower()) 
                   for col in available_columns]].rename(columns=lambda x: next(
                       k for k in new_data.keys() if k.lower() == x.lower()))
    logger.info(f"Extracted columns: {new_df.columns.tolist()}")
    return new_df

async def process_chunk(chunk, executor):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, extract_data, chunk)

async def process_excel_file(input_file, output_file, batch_size=10000):
    try:
        logger.info(f"Starting to process {input_file}")
        
        wb = load_workbook(filename=input_file, read_only=True)
        ws = wb.active
        
        # Log headers
        headers = [cell.value for cell in next(ws.rows)]
        logger.info(f"Input file headers: {headers}")
        
        # Log a sample row
        sample_row = [cell.value for cell in next(ws.rows)]
        logger.info(f"Sample row: {sample_row}")
        
        rows = []
        with ThreadPoolExecutor() as executor:
            tasks = []
            
            # Reset iterator after sampling
            ws._current_row = 1  # Reset to start after header
            next(ws.rows)  # Skip header again
            
            for i, row in enumerate(ws.rows, start=2):
                row_data = [cell.value for cell in row]
                rows.append(row_data)
                
                if len(rows) >= batch_size:
                    chunk_df = pd.DataFrame(rows, columns=headers)
                    tasks.append(process_chunk(chunk_df, executor))
                    rows = []
            
            if rows:
                chunk_df = pd.DataFrame(rows, columns=headers)
                tasks.append(process_chunk(chunk_df, executor))
            
            processed_chunks = await asyncio.gather(*tasks)
            
            if processed_chunks and any(not chunk.empty for chunk in processed_chunks):
                final_df = pd.concat([chunk for chunk in processed_chunks if not chunk.empty], 
                                   ignore_index=True)
                
                if not final_df.empty:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(executor, lambda: final_df.to_excel(
                        output_file, index=False, sheet_name='ProcessedData'))
                    logger.info(f"Dataset processed and saved to {output_file}")
                else:
                    logger.warning("Final DataFrame is empty; no file written.")
            else:
                logger.warning("No valid data processed.")
                
        wb.close()
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise
    finally:
        if 'wb' in locals():
            wb.close()

async def main():
    if not INPUT_FILE.exists():
        logger.error(f"Input file {INPUT_FILE} not found.")
        return
    
    await process_excel_file(INPUT_FILE, OUTPUT_FILE)

if __name__ == "__main__":
    asyncio.run(main())