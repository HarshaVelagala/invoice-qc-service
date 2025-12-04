import re
import json
import pdfplumber
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

RE_INVOICE_NO = re.compile(r"(?:Invoice\s*(?:No\.?|#|Number)[:\s]*)([A-Za-z0-9\-\/]+)", re.I)
RE_DATE = re.compile(r"(?:(?:Invoice\s*Date|Date)[:\s]*)(\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})", re.I)

def _parse_amount(s: str) -> Optional[float]:
    if not s: return None
    s = s.replace(",", "")
    try: return float(s)
    except: return None

def _parse_date(s: str) -> Optional[str]:
    if not s: return None
    for fmt in ["%d/%m/%Y","%d-%m-%Y","%Y-%m-%d","%d/%m/%y"]:
        try: return datetime.strptime(s, fmt).date().isoformat()
        except: pass
    return None

def extract_from_pdf(path: Path) -> Dict[str, Any]:
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            text += p.extract_text() or ""
            text += "\n"

    invoice_number = (m.group(1) if (m := RE_INVOICE_NO.search(text)) else None)
    invoice_date = _parse_date(m.group(1)) if (m := RE_DATE.search(text)) else None

    return {
        "invoice_id": path.stem,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "seller_name": "Unknown",
        "buyer_name": "Unknown",
        "net_total": None,
        "tax_amount": None,
        "gross_total": None,
        "line_items": []
    }

def extract_folder(pdf_dir: str, out_json: Optional[str] = None):
    folder = Path(pdf_dir)
    invoices = []

    for file in folder.glob("*.pdf"):
        invoices.append(extract_from_pdf(file))

    if out_json:
        with open(out_json, "w") as f:
            json.dump(invoices, f, indent=2)

    return invoices
