import requests
import pandas as pd

# URL of the Flask API endpoint
url = "http://127.0.0.1:5000/api"

# Define query parameters (modify as needed)
params = {"product_id": "product_1", "category_id": "cat_1", "region_id": "region_1"}

# Send a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)

    # Print the first few rows of the DataFrame
    print(df.head())
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
