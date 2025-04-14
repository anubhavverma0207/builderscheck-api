from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/run-redflag", methods=["POST"])
def run_redflag():
    data = request.get_json()
    name = data.get("name")

    # ✅ Get API keys from environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")

    if not name or not openai_key or not serpapi_key:
        return jsonify({"error": "Missing required parameters."}), 400

    # Create a temp filename for the report
    report_filename = f"redflag_report_{name.replace(' ', '_')}_v21.json"

    # Set environment variables temporarily for the subprocess
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = openai_key
    env["SERPAPI_API_KEY"] = serpapi_key

    # Run the redflag scraper script
    command = [
        "python", "redflag_scraper_ai_v21.py"
    ]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    # Feed the input values to the script
    stdout, stderr = process.communicate(input=f"{openai_key}\n{serpapi_key}\n{name}\n")

    # Check for error
    if process.returncode != 0:
        return jsonify({
            "error": "Scraper execution failed",
            "details": stderr
        }), 500

    # Return the report content
    try:
        with open(report_filename, "r", encoding="utf-8") as f:
            report_data = f.read()
        return jsonify({"report": report_data})
    except Exception as e:
        return jsonify({"error": "Report not found", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
