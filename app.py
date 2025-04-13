from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 CompanyHub API Credentials
COMPANYHUB_SUBDOMAIN = 'av0064380'
COMPANYHUB_API_KEY = 'O21heP2mMHn4EMrWY9DX'

@app.route('/get-companyhub-info', methods=['GET'])
def get_companyhub_info():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"error": "No company name provided"}), 400

    # Step 1: Prepare API request to CompanyHub
    url = f"https://api.companyhub.com/v1/tables/company?searchText={name}"
    headers = {
        "Authorization": f"{COMPANYHUB_SUBDOMAIN} {COMPANYHUB_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return jsonify({"error": f"Status {response.status_code}: {response.text}"}), 500

        data = response.json()

        # Step 2: Validate and extract data
        if not data.get("Success"):
            return jsonify({"error": data.get("Message", "Unknown error")}), 500

        records = data.get("Data", [])
        if not records:
            return jsonify({"error": "Company not found"}), 404

        # Step 3: Return the first matching record
        return jsonify(records[0])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def hello():
    return "BuilderCheck API is live ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
