import requests
import pandas as pd

# Fetch data from API
response = requests.get("https://api.energidataservice.dk/dataset/DeclarationProduction?start=2025-01-01&end=2025-06-01&filter={%22PriceArea%22:[%22DK1%22]}")

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Convert response to JSON

    # Extract the records from the JSON (adjust based on API structure)
    if "records" in data:
        df = pd.DataFrame(data["records"])

        # Save as CSV
        df.to_csv("energy_data.csv", index=False)
        print("CSV file saved as energy_data.csv")
    else:
        print("No 'records' key found in API response")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
