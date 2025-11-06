
import os, json, tempfile
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import yaml

from .extractors.invoice2data_runner import run_invoice2data
from .extractors.pdf_fallback import extract_with_pdfplumber
from .models import ExtractedData, CalculationRules
from .calculator import compute_net

app = FastAPI(title="Booking Netto API", version="0.2.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "extractors", "invoice2data_templates")
RULES_PATH = os.path.join(BASE_DIR, "config", "rules.yaml")

def load_rules() -> CalculationRules:
    with open(RULES_PATH, "r") as f:
        data = yaml.safe_load(f) or {}
    return CalculationRules(**data)

@app.post("/analyze")
async def analyze(files: List[UploadFile] = File(...), overrides: Optional[str] = Form(None)):
    rules = load_rules()
    try:
        overrides_dict: Dict[str, Any] = json.loads(overrides) if overrides else {}
    except Exception:
        overrides_dict = {}

    results = []
    for uf in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uf.filename)[1] or ".pdf") as tmp:
            content = await uf.read()
            tmp.write(content)
            tmp_path = tmp.name

        data = run_invoice2data(tmp_path, TEMPLATES_DIR)
        source = "invoice2data" if data else "pdf_fallback"
        if not data:
            data = extract_with_pdfplumber(tmp_path)

        for key in ("nights", "guests"):
            if key in overrides_dict:
                data[key] = overrides_dict[key]

        ex = ExtractedData(
            source=source,
            gross=data.get("gross"),
            commission=data.get("commission"),
            payout=data.get("payout"),
            nights=data.get("nights"),
            guests=data.get("guests"),
            raw=data
        )
        calc = compute_net(ex, rules)
        results.append({
            "file": uf.filename,
            "extracted": ex.model_dump(),
            "calculation": calc.model_dump(),
        })

        try:
            os.unlink(tmp_path)
        except Exception:
            pass

    return JSONResponse({"results": results})
