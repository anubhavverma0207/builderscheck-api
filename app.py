from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    name = request.args.get('name', '').lower()

    if not name:
        return jsonify({"error": "No company name provided"}), 400

    return jsonify({
        "message": "NZ Companies Register API integration coming soon.",
        "name": name
    })

@app.route('/check-companyhub', methods=['GET'])
def check_companyhub():
    name = request.args.get('name', '')
    url = f"https://www.companyhub.nz/nameCheck.cfm?name={name.replace(' ', '+')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Check for non-200 responses
        if response.status_code != 200:
            return jsonify({"error": f"Status {response.status_code}: Could not reach CompanyHub"}), 502

        soup = BeautifulSoup(response.text, 'html.parser')
        result_div = soup.find('div', class_='availabilityResult')

        message = result_div.get_text(strip=True) if result_div else "Could not find availability result"

        return jsonify({
            "companyhub_name_check": message
        })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
