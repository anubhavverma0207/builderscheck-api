from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Utility function to fetch and parse company data from NZ Companies Register
def get_nz_company_data(company_name):
    search_url = f"https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/search?q={company_name.replace(' ', '+')}"
    try:
        res = requests.get(search_url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return {"error": "Failed to access Companies Register"}

        soup = BeautifulSoup(res.text, 'html.parser')

        # Find company listing block
        result = soup.find("div", class_="result-table")
        if not result:
            return {"error": "Company not found"}

        first_row = result.find("tr", class_="odd") or result.find("tr", class_="even")
        if not first_row:
            return {"error": "No company data available"}

        cols = first_row.find_all("td")
        if len(cols) < 5:
            return {"error": "Incomplete data"}

        return {
            "companyName": cols[0].get_text(strip=True),
            "nzbn": cols[1].get_text(strip=True),
            "entityType": cols[2].get_text(strip=True),
            "status": cols[3].get_text(strip=True),
            "registrationDate": cols[4].get_text(strip=True)
        }

    except Exception as e:
        return {"error": str(e)}

# Flask route to access NZ company info
@app.route('/fetch-company-info', methods=['GET'])
def fetch_company():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"error": "Please provide a company name."}), 400

    data = get_nz_company_data(name)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
