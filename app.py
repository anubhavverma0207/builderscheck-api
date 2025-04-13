from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/fetch-company-info', methods=['GET'])
def fetch_company_info():
    company_name = request.args.get('name', '').strip()
    if not company_name:
        return jsonify({'error': 'No company name provided'}), 400

    # Step 1: Format search URL
    search_url = f"https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/search?mode=advanced&companyName={company_name.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Step 2: Make request to NZ Companies Register
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch from register'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Scrape list of companies from the search results
    companies = []
    rows = soup.select('table.searchResultTable tr')[1:]  # skip header
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            link = cols[0].find('a')
            name = link.text.strip()
            url = link['href']
            nzbn = cols[1].text.strip()
            status = cols[2].text.strip()
            companies.append({
                'name': name,
                'url': "https://app.companiesoffice.govt.nz" + url,
                'nzbn': nzbn,
                'status': status
            })

    # Step 4: Match company using case-insensitive partial match
    pattern = re.compile(re.escape(company_name), re.IGNORECASE)
    matched = next((c for c in companies if pattern.search(c['name'])), None)

    if not matched:
        return jsonify({"error": "Company not found"}), 404

    # Step 5: Scrape company details page
    details_response = requests.get(matched['url'], headers=headers)
    if details_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch company details'}), 500

    details_soup = BeautifulSoup(details_response.text, 'html.parser')

    info = {
        'companyName': matched['name'],
        'nzbn': matched['nzbn'],
        'status': matched['status'],
        'registrationDate': '',
        'entityType': '',
        'address': '',
    }

    try:
        info['registrationDate'] = details_soup.find(text='Incorporation Date:').find_next().text.strip()
        info['entityType'] = details_soup.find(text='Entity type:').find_next().text.strip()
        info['address'] = details_soup.find('a', href=True, text='Company addresses:').parent.find_next('td').text.strip()
    except Exception as e:
        print("Error parsing details:", e)

    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
