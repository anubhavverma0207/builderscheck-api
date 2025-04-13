from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "builderscheck-api is live!"

@app.route("/get-companyhub-info")
def get_companyhub_info():
    company_name = request.args.get("name")
    if not company_name:
        return jsonify({"error": "Missing 'name' query parameter"}), 400

    # Fetch environment variables
    subdomain = os.getenv("COMPANYHUB_SUBDOMAIN")
    api_key = os.getenv("COMPANYHUB_API_KEY")

    if not subdomain or not api_key:
        return jsonify({"error": "Missing COMPANYHUB_SUBDOMAIN or COMPANYHUB_API_KEY env variables"}), 500

    url = "https://api.companyhub.com/v1/tables/company/search"
    headers = {
        "Authorization": f"{subdomain} {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "Where": [
            {
                "FieldName": "Name",
                "Operator": "eq",
                "Values": [company_name]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
