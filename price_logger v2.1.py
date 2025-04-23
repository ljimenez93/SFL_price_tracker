import requests
import pandas as pd
from datetime import datetime, timezone
import os

# CONFIG
API_URL = "https://sfl.world/api/v1/prices"  # SFL API
OUTPUT_FILE = "prices.txt"  # Change to your desired path

def fetch_prices():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        prices = data['data']['p2p']

        # Extract and convert updatedAt to UTC timestamp string
        raw_timestamp = data["updatedAt"] / 1000  # convert from ms to s
        timestamp = datetime.fromtimestamp(raw_timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        return timestamp, prices
    except Exception as e:
        print(f"❌ Failed to fetch prices: {e}")
        return None, None

def log_prices():
    timestamp, prices = fetch_prices()
    if prices is None:
        return

    row_data = {'Timestamp': timestamp, **prices}
    df_new = pd.DataFrame([row_data])

    # If file exists, append new row
    if os.path.exists(OUTPUT_FILE):
        df_existing = pd.read_csv(OUTPUT_FILE)

        # Match new columns with existing ones
        df_new = df_new.reindex(columns=df_existing.columns, fill_value=None)

        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(OUTPUT_FILE, index=False)
    else:
        df_new.to_csv(OUTPUT_FILE, index=False)

    #print(f"✅ Logged prices at {timestamp} UTC")

if __name__ == "__main__":
    log_prices()
