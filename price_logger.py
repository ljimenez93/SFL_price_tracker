import requests
import json
from datetime import datetime
import os

API_URL = "https://sfl.world/api/v1/prices"
OUTPUT_FILE = "prices.txt"

def fetch_prices():
    """Fetches price data from the API."""
    if not API_URL:
        print("Error: API_URL environment variable not set.")
        return None
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if "data" in data and "p2p" in data["data"]:
            return data["data"]["p2p"]
        else:
            print(f"Error: Unexpected API response format: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def store_prices(prices):
    """Stores the fetched prices in a text file with timestamp."""
    if prices:
        timestamp = datetime.now().isoformat()
        with open(OUTPUT_FILE, "a") as f:
            for asset, price in prices.items():
                f.write(f"{asset},{price},{timestamp}\n")
        print(f"Prices stored successfully at {timestamp}")

if __name__ == "__main__":
    prices = fetch_prices()
    if prices:
        store_prices(prices)
