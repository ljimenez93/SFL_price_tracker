from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Replace this with your actual API URL
API_URL = "https://sfl.world/api/v1/prices"

@app.route("/prices", methods=["GET"])
def get_prices():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
