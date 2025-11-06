
#!/usr/bin/env python3
import time, json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys, yaml

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "app"))

from app.extractors.invoice2data_runner import run_invoice2data
from app.extractors.pdf_fallback import extract_with_pdfplumber
from app.models import ExtractedData, CalculationRules
from app.calculator import compute_net

DROPBOX_DIR = BASE_DIR / "assets" / "dropbox"
TEMPLATES_DIR = BASE_DIR / "app" / "extractors" / "invoice2data_templates"
RULES_PATH = BASE_DIR / "app" / "config" / "rules.yaml"

def load_rules() -> CalculationRules:
    with open(RULES_PATH, "r") as f:
        data = yaml.safe_load(f) or {}
    return CalculationRules(**data)

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.rules = load_rules()

    def on_created(self, event):
        if event.is_directory: return
        p = Path(event.src_path)
        if p.suffix.lower() != ".pdf": return
        try:
            data = run_invoice2data(str(p), str(TEMPLATES_DIR)) or extract_with_pdfplumber(str(p))
            source = "invoice2data" if data else "pdf_fallback"
            ex = ExtractedData(
                source=source,
                gross=data.get("gross"),
                commission=data.get("commission"),
                payout=data.get("payout"),
                nights=data.get("nights"),
                guests=data.get("guests"),
                raw=data
            )
            calc = compute_net(ex, self.rules)
            out_json = p.with_suffix(".analysis.json")
            out_txt = p.with_suffix(".netto.txt")
            out_json.write_text(json.dumps({"file": p.name, "extracted": ex.model_dump(), "calculation": calc.model_dump()}, ensure_ascii=False, indent=2), encoding="utf-8")
            out_txt.write_text(f"{calc.net_total} {calc.currency}\n", encoding="utf-8")
            print(f"[OK] {p.name} -> {out_txt.name}, {out_json.name}")
        except Exception as e:
            print(f"[ERR] {p.name}: {e}")

def main():
    DROPBOX_DIR.mkdir(parents=True, exist_ok=True)
    obs = Observer()
    obs.schedule(Handler(), str(DROPBOX_DIR), recursive=False)
    obs.start()
    print(f"Watching: {DROPBOX_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()

if __name__ == "__main__":
    main()
