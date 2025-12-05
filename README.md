Invoice QC Service – Harsha Velagala

A lightweight Invoice Extraction & Quality Control (QC) Service built as part of the DeepLogic AI Software Engineer Intern assignment.
The project reads PDF invoices, extracts structured data, validates them against defined business rules, and exposes the functionality through both a CLI tool and a FastAPI-based HTTP API.

🚀 Overview

This system includes the following major components:

✅ PDF Extraction Module
Extracts text from PDFs using pdfplumber and parses relevant fields into a structured JSON format.

✅ Validation Engine
Applies a set of completeness, formatting, and business rules (defined by me) to ensure data quality.

✅ CLI Interface
Provides commands to:
Extract invoices
Validate invoices
Run a full extract → validate pipeline

✅ HTTP API (FastAPI)
Endpoints include:
GET /health — Check system status
POST /validate-json — Validate invoices sent as JSON

✅ Deployment on Railway
The API is deployed and accessible at:
🔗 https://invoice-qc-service-production.up.railway.app

📄 Schema & Validation Design
To make the QC system realistic, I designed a simple but practical invoice schema.
Invoice Schema
Each invoice JSON object follows this structure:
Field	Description
invoice_id	Unique identifier derived from filename
invoice_number	Extracted invoice number
invoice_date	Date of invoice
seller_name	Name of seller
buyer_name	Name of buyer
net_total	Total before taxes
tax_amount	Tax/VAT
gross_total	Net + Tax
currency	Currency code (if detected)
line_items	List of items (optional, simplified as empty list)
Why line_items are simplified:
The provided PDFs did not contain structured tabular invoice items. Instead of forcing inaccurate extraction, I kept line items optional and empty.

Validation Rules
✔ Completeness Rules
invoice_number must be present
invoice_date must be present
seller_name and buyer_name cannot be empty

✔ Business Logic Rules
net_total + tax_amount ≈ gross_total
Totals cannot be negative

✔ Anomaly Rules
Duplicate invoices (same invoice_number) are flagged
These rules keep the QC process practical and easy to extend.

🏗 Architecture
PDFs → Extractor → JSON → Validator → CLI / API → Output
Folder Structure
invoice-qc-service/
│
├── invoice_qc/
│   ├── extractor.py
│   ├── validator.py
│   └── cli.py
│
├── app/
│   └── main.py
│
├── pdfs/                     # Test files
├── extracted.json            # Example extraction output
├── report.json               # Example validation output
├── requirements.txt
├── start.sh                  # Railway startup script
└── README.md

🖥 Usage (CLI)
Make sure your environment is activated:
source venv/bin/activate

1️⃣ Extract invoices
python -m invoice_qc.cli extract pdfs --output extracted.json

2️⃣ Validate invoices
python -m invoice_qc.cli validate extracted.json --report report.json

3️⃣ Full pipeline
python -m invoice_qc.cli full-run pdfs --report report.json

🌐 HTTP API
Base URL:
🔗 https://invoice-qc-service-production.up.railway.app
GET /health
Response:
{ "status": "ok" }
POST /validate-json
Validate one or more invoices.

Example Request:
[
  {
    "invoice_id": "TEST01",
    "invoice_number": "INV-001",
    "invoice_date": "2024-01-01",
    "net_total": 100,
    "tax_amount": 18,
    "gross_total": 118
  }
]

Example Response:
[
  {
    "invoice_id": "TEST01",
    "is_valid": true,
    "errors": []
  }
]

🔧 Deployment (Railway)
Deployment uses:
Procfile
web: bash start.sh
start.sh
#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
Railway automatically builds and serves the API.

🤖 AI Usage Notes
AI tools used:

ChatGPT for debugging, schema ideation, and API structuring
GitHub Copilot for auto-completion
Example where AI was incorrect:
AI initially generated overly complex table-extraction code assuming invoices had fully structured line items.
After reviewing the PDFs, I simplified the extractor to avoid extracting incorrect data.
⚠ Assumptions & Limitations
Sample PDFs were not real invoices → extraction is heuristic
Line items simplified due to lack of structured tabular content
Currency detection is limited
Validation rules can be expanded depending on business needs

🎥 Video Demo
(Will be added before submission)
🙌 Thank You
This project demonstrates backend engineering, data validation, and API design — and is structured so it can be easily extended by DeepLogic AI.
