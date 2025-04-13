from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Securely set these in environment variables for production
COMPANYHUB_API_KEY = "O21heP2mHNn4EMrWY9DX"
COMPANYHUB_SUBDOMAIN = "av0064380"

@app.route("/")
def home():
    return "BuilderCheck API is running!"

@app.route("/get-companyhub-info")
def get_companyhub_info():
    company_name = request.args.get("name")
    if not company_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    url = "https://api.companyhub.com/v1/tables/company/search"
    headers = {
        "Authorization": f"{COMPANYHUB_SUBDOMAIN} {COMPANYHUB_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "Where": [
            {
                "FieldName": "Name",
                "Operator": "eq",
                "Values": [company_name]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
