from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    query = request.args.get('name', '').lower().strip()
    if not query:
        return jsonify({"error": "Company name is required"}), 400

    try:
        search_url = f"https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/search?mode=standard&type=entities&q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Step 1: Perform the search
        search_resp = requests.get(search_url, headers=headers)
        if search_resp.status_code != 200:
            return jsonify({"error": "Failed to connect to NZ Companies Register"}), 502

        # Step 2: Extract company IDs from search results
        soup = BeautifulSoup(search_resp.text, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'/companies/app/ui/pages/companies/(\d+)/'))

        matched_company_id = None
        matched_name = None

        for link in links:
            name = link.get_text(strip=True).lower()
            if query in name:
                matched_company_id = re.search(r'/companies/app/ui/pages/companies/(\d+)/', link['href']).group(1)
                matched_name = link.get_text(strip=True)
                break

        if not matched_company_id:
            return jsonify({"error": "Company not found"}), 404

        # Step 3: Scrape company details
        company_url = f"https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/{matched_company_id}/"
        company_resp = requests.get(company_url, headers=headers)
        if company_resp.status_code != 200:
            return jsonify({"error": "Failed to load company details"}), 502

        company_soup = BeautifulSoup(company_resp.text, 'html.parser')

        # Scrape details from the main info page
        def get_text_by_label(label):
            el = company_soup.find("div", string=re.compile(label, re.I))
            if el and el.find_next("div"):
                return el.find_next("div").get_text(strip=True)
            return None

        return jsonify({
            "companyName": matched_name,
            "nzbn": get_text_by_label("NZBN"),
            "status": get_text_by_label("Status"),
            "registrationDate": get_text_by_label("Incorporation Date") or get_text_by_label("Registered"),
            "entityType": get_text_by_label("Entity Type"),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
