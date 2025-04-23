import os
import csv
import requests
from datetime import datetime, timezone

# Your API URL
url = "https://sfl.world/api/v1/prices"  # <- Replace with your real API

try:
    response = requests.get(url)
    data = response.json()

    # Convert timestamp from API to UTC datetime
    timestamp = datetime.fromtimestamp(data["updatedAt"] / 1000, tz=timezone.utc)
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    date_str = timestamp.strftime('%Y-%m-%d')  # for filename

    # Get asset data
    assets = data["data"]["p2p"]
    asset_names = list(assets.keys())
    asset_values = list(assets.values())

    # Prepare folder and filename
    os.makedirs("prices", exist_ok=True)
    file_path = f"prices/{date_str}.csv"

    # Write header if file doesn't exist
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp"] + asset_names)
        writer.writerow([formatted_time] + asset_values)

    print(f"✅ Logged prices to {file_path}")

except Exception as e:
    print(f"❌ Error: {e}")
