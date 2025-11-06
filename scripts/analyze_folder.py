
#!/usr/bin/env python3
import os, sys, csv, json, argparse, glob
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))
from app.extractors.invoice2data_runner import run_invoice2data
from app.extractors.pdf_fallback import extract_with_pdfplumber
from app.models import ExtractedData, CalculationRules
from app.calculator import compute_net
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = BASE_DIR / "app" / "extractors" / "invoice2data_templates"
RULES_PATH = BASE_DIR / "app" / "config" / "rules.yaml"

def load_rules() -> CalculationRules:
    with open(RULES_PATH, "r") as f:
        data = yaml.safe_load(f) or {}
    return CalculationRules(**data)

def analyze_one(pdf_path: Path, rules: CalculationRules):
    data = run_invoice2data(str(pdf_path), str(TEMPLATES_DIR))
    source = "invoice2data" if data else "pdf_fallback"
    if not data:
        data = extract_with_pdfplumber(str(pdf_path))
    ex = ExtractedData(
        source=source,
        gross=data.get("gross"),
        commission=data.get("commission"),
        payout=data.get("payout"),
        nights=data.get("nights"),
        guests=data.get("guests"),
        raw=data,
    )
    calc = compute_net(ex, rules)
    return ex, calc

def main():
    ap = argparse.ArgumentParser(description="Analyze a folder of PDFs and save results to CSV/JSON.")
    ap.add_argument("folder", help="Folder containing PDFs")
    ap.add_argument("--csv", default="report.csv", help="Output CSV path")
    ap.add_argument("--jsonl", default="report.jsonl", help="Output JSONL path")
    args = ap.parse_args()

    rules = load_rules()
    pdfs = sorted(glob.glob(os.path.join(args.folder, "*.pdf")))

    rows = []
    with open(args.jsonl, "w", encoding="utf-8") as jf:
        for p in pdfs:
            ex, calc = analyze_one(Path(p), rules)
            row = {
                "file": os.path.basename(p),
                "gross": calc.gross_total,
                "commission": calc.computed_commission,
                "iva": calc.iva_amount,
                "city_tax": calc.city_tax_total,
                "fixed_costs": calc.fixed_costs_total,
                "net": calc.net_total,
                "currency": calc.currency,
                "nights": ex.nights,
                "guests": ex.guests,
                "source": ex.source,
            }
            rows.append(row)
            jf.write(json.dumps({"file": os.path.basename(p), "extracted": ex.model_dump(), "calculation": calc.model_dump()}, ensure_ascii=False) + "\n")

    if rows:
        keys = ["file","gross","commission","iva","city_tax","fixed_costs","net","currency","nights","guests","source"]
        with open(args.csv, "w", newline="", encoding="utf-8") as cf:
            w = csv.DictWriter(cf, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow(r)
    print(f"Processed {len(rows)} PDF(s). CSV -> {args.csv}, JSONL -> {args.jsonl}")

if __name__ == "__main__":
    main()
