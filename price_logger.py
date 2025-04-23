import os
import csv
import requests
from datetime import datetime, timezone

# Your API URL
url = "https://sfl.world/api/v1/prices"  # SFL API

try:
    response = requests.get(url)
    data = response.json()

    # Convert API timestamp to UTC datetime
    timestamp = datetime.fromtimestamp(data["updatedAt"] / 1000, tz=timezone.utc)
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # Extract asset prices
    prices = data["data"]["p2p"]
    asset_names = list(prices.keys())
    asset_values = [prices[a] for a in asset_names]

    file_path = "prices.txt"

    # Create or update the file
    if not os.path.exists(file_path):
        # First time: create file with header
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp"] + asset_names)
            writer.writerow([formatted_time] + asset_values)
    else:
        # Merge new column with existing file
        with open(file_path, newline='') as f:
            reader = list(csv.reader(f))

        # Append new column to the existing file
        header = reader[0]
        rows = reader[1:]

        if header[0] != "Timestamp":
            raise Exception("Invalid file format: first column must be 'Timestamp'")

        if len(rows) != len(asset_values):
            raise Exception("Mismatch between row count and asset count")

        # Add new column name to header
        header.append(formatted_time)

        # Add new price value to each row
        for i, row in enumerate(rows):
            row.append(asset_values[i])

        # Write updated content back to the file
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

    print(f"✅ Prices updated in {file_path}")

except Exception as e:
    print(f"❌ Error: {e}")
