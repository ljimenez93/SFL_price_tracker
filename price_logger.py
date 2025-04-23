from datetime import datetime, timezone
import requests
import csv
import os

# API URL (replace with your real endpoint)
url = "https://sfl.world/api/v1/prices"  # <-- UPDATE THIS

try:
    response = requests.get(url)
    data = response.json()

    # Get UTC timestamp from API
    timestamp = datetime.fromtimestamp(data["updatedAt"] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # Extract prices
    assets = data["data"]["p2p"]
    asset_names = list(assets.keys())
    asset_values = list(assets.values())

    # Define output file path
    file_path = "prices.txt"

    # Check if file exists and has a header
    file_exists = os.path.isfile(file_path)
    header_needed = not file_exists or os.stat(file_path).st_size == 0

    # Write to file
    with open(file_path, "a", newline='') as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["Timestamp"] + asset_names)
        writer.writerow([timestamp] + asset_values)

    print("✅ Prices saved successfully.")

except Exception as e:
    print(f"❌ Error: {e}")
