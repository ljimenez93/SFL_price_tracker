import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone
import json
import os

# Load service account credentials from GitHub secret
creds_json = os.environ.get("GOOGLE_SHEETS_CREDS")
creds_dict = json.loads(creds_json)

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("SFL Price Tracker").worksheet("Prices")  # Adjust name as needed

# Fetch API data
url = "https://sfl.world/api/v1/prices"  # API URL
response = requests.get(url)
data = response.json()

# Extract UTC timestamp and format it
timestamp = datetime.fromtimestamp(data["updatedAt"] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Extract asset prices
prices = data["data"]["p2p"]
assets = list(prices.keys())
values = list(prices.values())

# Read existing headers (first row)
header = sheet.row_values(1)

# If first column is empty, set up headers
if not header:
    sheet.append_row(["Timestamp"] + assets)
else:
    # If new assets appear later, extend headers
    for asset in assets:
        if asset not in header:
            header.append(asset)
            sheet.update_cell(1, len(header), asset)

# Create full row with values in correct columns
row = [timestamp]
for asset in header[1:]:
    value = prices.get(asset, "")
    print(f"{asset}: {value}")
    row.append(value)

# Append row to sheet
sheet.append_row(row)
