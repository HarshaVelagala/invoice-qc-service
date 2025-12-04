from typing import List, Dict, Any
import math

def validate_invoice(inv: Dict[str, Any]) -> Dict[str, Any]:
    errors = []

    # Completeness checks
    if not inv.get("invoice_number"):
        errors.append("missing_invoice_number")

    if not inv.get("invoice_date"):
        errors.append("missing_invoice_date")

    # Business rule: totals must match
    net = inv.get("net_total")
    tax = inv.get("tax_amount")
    gross = inv.get("gross_total")

    if net is not None and tax is not None and gross is not None:
        try:
            if not math.isclose(float(net) + float(tax), float(gross), abs_tol=1.0):
                errors.append("totals_mismatch")
        except:
            errors.append("totals_invalid_format")

    return {
        "invoice_id": inv["invoice_id"],
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def validate_all(invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = [validate_invoice(inv) for inv in invoices]

    summary = {
        "total": len(results),
        "valid": sum(1 for r in results if r["is_valid"]),
        "invalid": sum(1 for r in results if not r["is_valid"]),
        "error_counts": {}
    }

    # Count frequency of each error
    for r in results:
        for err in r["errors"]:
            summary["error_counts"][err] = summary["error_counts"].get(err, 0) + 1

    return {
        "summary": summary,
        "invoices": results
    }
