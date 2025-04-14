# ✅ app.py
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/run-redflag", methods=["POST"])
def run_redflag():
    data = request.get_json()
    name = data.get("name")
    openai_key = data.get("openai_key")
    serpapi_key = data.get("serpapi_key")

    if not name or not openai_key or not serpapi_key:
        return jsonify({"error": "Missing required parameters."}), 400

    # Save keys as environment variables
    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["SERPAPI_API_KEY"] = serpapi_key

    # Run the scraper script
    process = subprocess.Popen(
        ["python", "redflag_scraper_ai_v21.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=f"{openai_key}\n{serpapi_key}\n{name}\n")

    if process.returncode != 0:
        return jsonify({"error": "Scraper execution failed", "details": stderr}), 500

    try:
        filename = f"redflag_report_{name.replace(' ', '_')}_v21.json"
        with open(filename, "r", encoding="utf-8") as f:
            return jsonify({"report": f.read()})
    except Exception as e:
        return jsonify({"error": "Report not found", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
