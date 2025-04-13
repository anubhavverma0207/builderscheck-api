from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Static values from your CompanyHub account
API_KEY = "O21heP2mHNn4EMrWY9DX"
SUBDOMAIN = "av0064380"

@app.route("/get-companyhub-info", methods=["GET"])
def get_companyhub_info():
    company_name = request.args.get("name")
    if not company_name:
        return jsonify({"error": "Missing company name in query parameters."}), 400

    url = "https://api.companyhub.com/v1/tables/company/search"

    headers = {
        "Authorization": f"{SUBDOMAIN} {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "Where": [
            {
                "FieldName": "Name",
                "Operator": "cn",  # 'cn' = contains
                "Values": [company_name]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
