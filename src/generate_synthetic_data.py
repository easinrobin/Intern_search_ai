import pandas as pd
import random
from faker import Faker
import string

# Initialize Faker for generating realistic text
fake = Faker()

# Lists for generating realistic electronics data
categories = [
    'Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Smart Watches',
    'Televisions', 'Cameras', 'Speakers', 'Gaming Consoles', 'Accessories'
]

brands = [
    'TechTrend', 'InnoVibe', 'SmartPeak', 'ElectroNova', 'GizmoCore',
    'PulseTech', 'VisionQuest', 'SonicWave', 'GameSphere', 'ConnectPlus'
]

# Function to generate SKU
def generate_sku(category, index):
    cat_code = category[:3].upper()
    return f"{cat_code}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}-{index:04d}"

# Generate the dataset
data = {
    'Name': [],
    'Category': [],
    'Price': [],
    'Stock Quantity': [],
    'Short Description': [],
    'Long Description': [],
    'SKU': []
}

for i in range(10000):
    category = random.choice(categories)
    brand = random.choice(brands)
    
    # Generate product name based on category
    if category == 'Smartphones':
        name = f"{brand} Phone {random.randint(10, 15)} Pro"
    elif category == 'Laptops':
        name = f"{brand} Book {random.randint(300, 500)}"
    elif category == 'Tablets':
        name = f"{brand} Tab {random.choice(['Air', 'Pro', 'Mini'])}"
    elif category == 'Headphones':
        name = f"{brand} Audio {random.choice(['X', 'Plus', 'Elite'])}"
    elif category == 'Smart Watches':
        name = f"{brand} Watch {random.randint(4, 8)}"
    elif category == 'Televisions':
        name = f"{brand} Vision {random.randint(40, 85)} inch"
    elif category == 'Cameras':
        name = f"{brand} Cam {random.choice(['DSLR', 'Mirrorless', 'Point'])}"
    elif category == 'Speakers':
        name = f"{brand} Sound {random.choice(['Boom', 'Echo', 'Pulse'])}"
    elif category == 'Gaming Consoles':
        name = f"{brand} Play {random.randint(5, 7)}"
    else:  # Accessories
        name = f"{brand} {random.choice(['Charger', 'Cable', 'Case', 'Hub'])}"

    # Generate other fields
    price = round(random.uniform(29.99, 1999.99), 2)
    stock = random.randint(0, 500)
    short_desc = f"High-quality {category.lower()} with {random.choice(['advanced', 'cutting-edge', 'modern'])} features"
    long_desc = fake.paragraph(nb_sentences=3)
    sku = generate_sku(category, i + 1)

    # Append to data dictionary
    data['Name'].append(name)
    data['Category'].append(category)
    data['Price'].append(price)
    data['Stock Quantity'].append(stock)
    data['Short Description'].append(short_desc)
    data['Long Description'].append(long_desc)
    data['SKU'].append(sku)

# Create DataFrame
df = pd.DataFrame(data)

# Export to Excel
output_file = 'electronics_products_10k.xlsx'
df.to_excel(output_file, index=False)

print(f"Dataset with 10,000 products has been generated and saved as '{output_file}'")