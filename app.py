from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Constants
COMPANYHUB_API_BASE = "https://api.companyhub.com/v1"
SUBDOMAIN = "av0064380"
API_KEY = "O21heP2mHNn4EMrWY9DX"
HEADERS = {
    "Authorization": f"{SUBDOMAIN} {API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/get-companyhub-info', methods=['GET'])
def get_companyhub_info():
    company_name = request.args.get('name')
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    try:
        url = f"{COMPANYHUB_API_BASE}/tables/company/search"
        body = {
            "Where": [
                {
                    "FieldName": "Name",
                    "Operator": "eq",
                    "Values": [company_name]
                }
            ]
        }

        response = requests.post(url, json=body, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return jsonify({"error": f"Status {response.status_code}: {response.text}"}), response.status_code

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "BuilderCheck API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
