from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration
API_KEY = os.environ.get("COMPANYHUB_API_KEY", "O21heP2mHNn4EMrWY9DX")
SUBDOMAIN = os.environ.get("COMPANYHUB_SUBDOMAIN", "av0064380")

COMPANYHUB_SEARCH_URL = "https://api.companyhub.com/v1/tables/company/search"
HEADERS = {
    "Authorization": f"{SUBDOMAIN} {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return "BuildersCheck API is running"

@app.route("/get-companyhub-info", methods=["GET"])
def get_companyhub_info():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Missing 'name' query parameter"}), 400

    payload = {
        "Where": [
            {
                "FieldName": "Name",
                "Operator": "eq",
                "Values": [name]
            }
        ]
    }

    try:
        response = requests.post(COMPANYHUB_SEARCH_URL, headers=HEADERS, json=payload)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
