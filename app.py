from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# CompanyHub API configuration
COMPANYHUB_SUBDOMAIN = "av0064380"
COMPANYHUB_API_KEY = "O21heP2mMHn4EMrWY9DX"
COMPANYHUB_BASE_URL = "https://api.companyhub.com/v1"

@app.route("/get-companyhub-info", methods=["GET"])
def get_companyhub_info():
    company_name = request.args.get("name")
    if not company_name:
        return jsonify({"error": "Missing company name parameter"}), 400

    # Prepare API request to CompanyHub search
    url = f"{COMPANYHUB_BASE_URL}/tables/company?searchText={company_name}"
    headers = {
        "Authorization": f"{COMPANYHUB_SUBDOMAIN} {COMPANYHUB_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return jsonify({"error": f"Status {response.status_code}: {response.text}"}), response.status_code

        data = response.json()
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "CompanyHub API Integration Active"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
