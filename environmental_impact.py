import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def calculate_impact(consumption_kwh):
    # Your API token
    token = 'mkghuvLIc24M7'

    # Define the API endpoint and headers
    url = 'https://api.electricitymap.org/v3/carbon-intensity/latest?zone=SG' #Adjusted for Singapore (for Collab)
    # url = 'https://api.electricitymap.org/v3/carbon-intensity/latest?zone=FR' #Adjusted for France (for Local)
    headers = {
        'auth-token': token
    }

    # Print URL and headers for debugging
    print(f"URL: {url}")
    print(f"Headers: {headers}")

    # Set up retry strategy
    retry_strategy = Retry(
        total=3,  # Number of retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        # Make the request to the API
        response = http.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            print("Data fetched successfully!")
            print("Response JSON:", data)  # Print the entire JSON response
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return

        # Access the carbon intensity value
        carbon_intensity = data['carbonIntensity']  # Adjust based on actual JSON structure

        # Calculate the total CO2 emissions
        total_emissions = consumption_kwh * carbon_intensity / 1000  # Convert to kgCO2eq

        print(f"Total CO2 emissions for {consumption_kwh} kWh: {total_emissions} kgCO2eq")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
# calculate_impact(consumption_kwh=1.325)