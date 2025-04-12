
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search-company', methods=['GET'])
def search_company():
    name = request.args.get('name', '').lower()

    if name == "cavalier":
        return jsonify({
            "companyName": "Cavalier Homes Auckland South Limited",
            "nzbn": "9429034567890",
            "status": "Removed",
            "registrationDate": "2008-05-14",
            "entityType": "Limited Liability Company",
            "directors": [{"name": "Wade Eatts", "appointed": "2008-05-14"}],
            "redFlags": [
                "Company is deregistered",
                "Director has other failed entities"
            ]
        })
    else:
        return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
