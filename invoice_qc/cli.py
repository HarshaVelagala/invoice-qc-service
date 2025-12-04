import typer
import json
from invoice_qc.extractor import extract_folder
from invoice_qc.validator import validate_all

app = typer.Typer()

@app.command()
def extract(pdf_dir: str, output: str = "extracted.json"):
    invoices = extract_folder(pdf_dir, out_json=output)
    typer.echo(f"Extracted {len(invoices)} invoices → {output}")


@app.command()
def validate(input: str, report: str = "report.json"):
    with open(input) as f:
        invoices = json.load(f)

    result = validate_all(invoices)

    with open(report, "w") as f:
        json.dump(result, f, indent=2)

    typer.echo(
        f"Valid: {result['summary']['valid']}, Invalid: {result['summary']['invalid']}"
    )


@app.command()
def full_run(pdf_dir: str, report: str = "report.json"):
    invoices = extract_folder(pdf_dir)

    result = validate_all(invoices)

    with open(report, "w") as f:
        json.dump(result, f, indent=2)

    typer.echo(
        f"Full pipeline completed! Valid: {result['summary']['valid']}, Invalid: {result['summary']['invalid']}"
    )


if __name__ == "__main__":
    app()
