from datetime import datetime, timezone
import requests
import csv
import os

url = "https://sfl.world/api/v1/prices"  # Replace with your real URL
response = requests.get(url)
data = response.json()

# Get UTC timestamp from API
timestamp = datetime.fromtimestamp(data["updatedAt"] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

assets = data["data"]["p2p"]
file_exists = os.path.isfile("prices.txt")

with open("prices.txt", "a", newline='') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Timestamp"] + list(assets.keys()))
    writer.writerow([timestamp] + list(assets.values()))
