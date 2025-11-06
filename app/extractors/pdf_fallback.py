
import re
from typing import Dict, Any, Optional
import pdfplumber

NUM = r"[0-9][0-9\.,\s]*"

PATTERNS = {
    "gross": re.compile(r"(?i)(total|amount|totale)\D{0,12}(" + NUM + ")"),
    "commission": re.compile(r"(?i)(commission|commissioni)\D{0,12}(" + NUM + ")"),
    "payout": re.compile(r"(?i)(payout|pagamento|netto)\D{0,12}(" + NUM + ")"),
    "nights": re.compile(r"(?i)(nights|notti)\D{0,12}([0-9]+)"),
    "guests": re.compile(r"(?i)(guests|ospiti|persone)\D{0,12}([0-9]+)"),
}

def _norm_number(s: str) -> float:
    s = s.strip().replace(' ', '')
    if s.count(",") == 1 and s.count(".") >= 1 and s.rfind(",") > s.rfind("."):
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") > 1 and "," not in s:
        s = s.replace(".", "")
    elif "," in s and "." not in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s)

def _extract_first(pattern, text) -> Optional[str]:
    m = pattern.search(text)
    if not m:
        return None
    return m.group(2)

def extract_with_pdfplumber(pdf_path: str) -> Dict[str, Any]:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            text += "\n" + txt

    result: Dict[str, Any] = {}
    for key, pat in PATTERNS.items():
        val = _extract_first(pat, text)
        if val:
            try:
                if key in ("nights", "guests"):
                    result[key] = int(val)
                else:
                    result[key] = _norm_number(val)
            except:
                pass
    return result
