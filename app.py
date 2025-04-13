from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Endpoint: Default placeholder for Companies Office NZ (coming soon)
@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    name = request.args.get('name', '').lower()
    if not name:
        return jsonify({"error": "No company name provided"}), 400
    return jsonify({
        "message": "NZ Companies Register API integration coming soon.",
        "name": name
    })

# Endpoint: Check CompanyHub UI screen-scraped availability result
@app.route('/check-companyhub', methods=['GET'])
def check_companyhub():
    name = request.args.get('name', '')
    url = f"https://www.companyhub.nz/nameCheck.cfm?name={name.replace(' ', '+')}"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        result_div = soup.find('div', class_='availabilityResult')
        message = result_div.get_text(strip=True) if result_div else "Could not find availability result"
        return jsonify({ "companyhub_name_check": message })
    except Exception as e:
        return jsonify({ "error": f"Status 403: Could not reach CompanyHub" }), 403

# ✅ NEW Endpoint: Query CompanyHub's API via exact match using field filters
@app.route('/get-companyhub-info', methods=['GET'])
def get_companyhub_info():
    company_name = request.args.get('name', '')
    url = "https://api.companyhub.com/v1/tables/company/search"

    headers = {
        "Authorization": "av0064380 O21heP2mHNn4EMrWY9DX",  # Replace with your subdomain and API key
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
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

# Flask server run block
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
