from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Environment variables (replace with your actual values or manage via Render's dashboard)
COMPANYHUB_API_KEY = "O21heP2mHNn4EMrWY9DX"
SUBDOMAIN = "av0064380"
API_URL = f"https://api.companyhub.com/v1/tables/company/search"

@app.route('/')
def home():
    return "BuilderCheck API is running."

@app.route('/get-companyhub-info', methods=['GET'])
def get_companyhub_info():
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Missing 'name' parameter."}), 400

        headers = {
            "Authorization": f"{SUBDOMAIN} {COMPANYHUB_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "Where": [
                {
                    "FieldName": "Name",
                    "Operator": "eq",
                    "Values": [name]
                }
            ]
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Render fix: Bind to provided PORT env var (or fallback to 5000 for local)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
