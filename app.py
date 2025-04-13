from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

COMPANYHUB_SUBDOMAIN = 'av0064380'
COMPANYHUB_API_KEY = 'O21heP2mMHn4EMrWY9DX'

@app.route('/get-companyhub-info', methods=['GET'])
def get_companyhub_info():
    company_name = request.args.get('name', '')

    if not company_name:
        return jsonify({"error": "No company name provided"}), 400

    url = f"https://api.companyhub.com/v1/tables/company?searchText={company_name}"

    headers = {
        "Authorization": f"{COMPANYHUB_SUBDOMAIN} {COMPANYHUB_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Status {response.status_code}: {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
