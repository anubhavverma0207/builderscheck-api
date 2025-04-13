from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    name = request.args.get('name', '').lower()

    # Simple fallback if company not provided
    if not name:
        return jsonify({"error": "No company name provided"}), 400

    return jsonify({
        "message": "NZ Companies Register scraping currently under maintenance. Use /check-companyhub for name check.",
        "name": name
    })

@app.route('/check-companyhub', methods=['GET'])
def check_companyhub():
    name = request.args.get('name', '')
    url = f"https://www.companyhub.nz/nameCheck.cfm?name={name.replace(' ', '+')}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # The result is inside the input box or result section
        result_div = soup.find('div', class_='results') or soup.find('div', class_='availabilityResult')
        message = result_div.get_text(strip=True) if result_div else "Could not find availability result"

        return jsonify({
            "companyhub_name_check": message
        })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
