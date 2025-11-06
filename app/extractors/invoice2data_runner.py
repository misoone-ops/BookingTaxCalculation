
from typing import Optional, Dict, Any
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates

def run_invoice2data(pdf_path: str, templates_dir: str) -> Optional[Dict[str, Any]]:
    try:
        templates = read_templates(templates_dir)
        data = extract_data(pdf_path, templates=templates)
        return data or None
    except Exception:
        return None
