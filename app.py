
from flask import Flask, request, jsonify, make_response
import io
from fpdf import FPDF

app = Flask(__name__)

@app.route('/search-company', methods=['GET'])
def search_company():
    name = request.args.get('name', '').lower()

    if name == 'cavalier':
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

@app.route('/download-report', methods=['GET'])
def download_report():
    name = request.args.get('name', '').lower()

    if name == 'cavalier':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Builder Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt="Company Name: Cavalier Homes Auckland South Limited", ln=True)
        pdf.cell(200, 10, txt="NZBN: 9429034567890", ln=True)
        pdf.cell(200, 10, txt="Status: Removed", ln=True)
        pdf.cell(200, 10, txt="Entity Type: Limited Liability Company", ln=True)
        pdf.cell(200, 10, txt="Director: Wade Eatts (Appointed: 2008-05-14)", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt="Red Flags:", ln=True)
        pdf.cell(200, 10, txt=" - Company is deregistered", ln=True)
        pdf.cell(200, 10, txt=" - Director has other failed entities", ln=True)

        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        return make_response(pdf_output.read(), {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename=builder_report.pdf'
        })
    else:
        return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
