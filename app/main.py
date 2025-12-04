from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from invoice_qc.validator import validate_all

app = FastAPI()

class InvoiceModel(BaseModel):
    invoice_id: str
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    seller_name: Optional[str] = None
    buyer_name: Optional[str] = None
    net_total: Optional[float] = None
    tax_amount: Optional[float] = None
    gross_total: Optional[float] = None
    line_items: list = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validate-json")
def validate_json(invoices: List[Dict[str, Any]]):
    result = validate_all(invoices)
    return result
