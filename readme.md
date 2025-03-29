# Intent-Based Product Search with AI

This project implements an **Intent-Based Product Search** using **Artificial Intelligence**. The goal is to provide a more accurate and intelligent way to search for products by understanding the **user's intent** rather than just relying on keywords. The search engine utilizes AI to interpret the meaning behind a user's query and return the most relevant products.

## Features

- AI-powered product search based on user intent
- Easy-to-use web interface for searching
- Supports querying based on product attributes, categories, and user preferences

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.13+
- `pip` (Python package installer)

## Installation

Follow the steps below to install dependencies and set up the project.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/intent-based-product-search.git
cd intent-based-product-search
```

### 2. Set Up a Virtual Environment
It's recommended to use a virtual environment to isolate your project dependencies:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
After activating the virtual environment, install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
This will install all the necessary Python packages.

### 4. Running the Project
To run the project, follow these steps:

#### 1. Prepare the Data
First, run prepare_data.py to preprocess and load the data for the AI model. This step will set up the necessary datasets and configurations required for the search functionality.
```bash
python prepare_data.py
```

#### 2. Run the Application
Once the data is prepared, run app.py to start the application. It will open a web server on a specified port (default is localhost:5000) to access the search functionality via a browser.
```bash
python app.py
```
After running the above command, you can open your browser and visit http://localhost:5000 to interact with the search interface.