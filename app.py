from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_company_info_from_nz_register(company_name):
    search_url = f"https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/search?mode=default"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Step 1: Search the Companies Register
    session = requests.Session()
    response = session.get(f"https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/search?mode=default&searchTerm={company_name}", headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select("table#searchResultsTable tbody tr")

    for row in results:
        name_cell = row.select_one("td a")
        if not name_cell:
            continue
        matched_name = name_cell.text.strip().lower()
        if company_name.lower() in matched_name:
            href = name_cell.get('href')
            company_url = f"https://app.companiesoffice.govt.nz{href}"

            # Step 2: Scrape company detail page
            detail_res = session.get(company_url, headers=headers)
            if detail_res.status_code != 200:
                return None

            detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
            company_info = {
                "companyName": detail_soup.select_one("#companyHeading").text.strip() if detail_soup.select_one("#companyHeading") else None,
                "nzbn": detail_soup.find("th", string="NZBN:").find_next("td").text.strip() if detail_soup.find("th", string="NZBN:") else None,
                "registrationDate": detail_soup.find("th", string="Incorporation Date:").find_next("td").text.strip() if detail_soup.find("th", string="Incorporation Date:") else None,
                "status": detail_soup.find("th", string="Company Status:").find_next("td").text.strip() if detail_soup.find("th", string="Company Status:") else None,
                "entityType": detail_soup.find("th", string="Entity type:").find_next("td").text.strip() if detail_soup.find("th", string="Entity type:") else None,
            }
            return company_info

    return None

@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"error": "Company name is required"}), 400

    result = fetch_company_info_from_nz_register(name)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
