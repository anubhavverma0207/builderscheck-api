from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/search-company', methods=['GET'])
def search_company():
    name = request.args.get('name', '').lower()
    if name == 'cavalier':
        return jsonify({
            "companyName": "Cavalier Homes Auckland South Limited",
            "nzbnh": "9429034567890",
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

@app.route('/download-report', methods=['GET'])
def download_report():
    name = request.args.get('name', '').lower()
    if name != 'cavalier':
        return jsonify({"error": "Company not found"}), 404

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Company Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Name: Cavalier Homes Auckland South Limited", ln=True)
    pdf.cell(200, 10, txt="NZBN: 9429034567890", ln=True)
    pdf.cell(200, 10, txt="Status: Removed", ln=True)
    pdf.cell(200, 10, txt="Registered: 2008-05-14", ln=True)
    pdf.cell(200, 10, txt="Director: Wade Eatts", ln=True)
    pdf.cell(200, 10, txt="Red Flags: Company is deregistered, Director has other failed entities", ln=True)

    # Save to file temporarily
    filepath = "/tmp/company_report.pdf"
    pdf.output(filepath)

    # Send file
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
