from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    company_name = request.args.get('name', '').strip()

    if not company_name:
        return jsonify({"error": "Missing company name"}), 400

    try:
        # Call hidden NZ Companies Office API
        search_url = "https://app.companiesoffice.govt.nz/companies/app/ui/search/companies"
        params = {
            "mode": "advanced",
            "searchTerm": company_name
        }
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, params=params, headers=headers)
        data = response.json()

        if not data.get("items"):
            return jsonify({"error": "Company not found"}), 404

        # Take the best matching company (first one)
        company = data["items"][0]

        result = {
            "companyName": company.get("companyName"),
            "nzbn": company.get("nzbn"),
            "companyNumber": company.get("companyNumber"),
            "status": company.get("status"),
            "incorporationDate": company.get("incorporationDate")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
