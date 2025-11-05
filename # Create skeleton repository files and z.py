# Create skeleton repository files and zip them for download

import os, textwrap, json, zipfile, io, pathlib

base = "/Users/simonecarta/Documents/BookingTaxCalculation/"
os.makedirs(base, exist_ok=True)

# Directory structure
dirs = [
    "app",
    "app/extractors/invoice2data_templates",
    "app/extractors",
    "app/config",
    "tests",
]
for d in dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)

# .gitignore
gitignore = textwrap.dedent("""
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
.venv/
.env

# macOS
.DS_Store

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
""")
open(os.path.join(base, ".gitignore"), "w").write(gitignore)

# requirements.txt
requirements = textwrap.dedent("""
fastapi>=0.115
uvicorn[standard]>=0.30
pydantic>=2.6
pandas>=2.0
pdfplumber>=0.11
invoice2data>=0.5
PyYAML>=6.0

# Opzionali (scommenta se necessario per tabelle complesse)
# camelot-py[cv]>=0.11
# tabula-py>=2.9
""")
open(os.path.join(base, "requirements.txt"), "w").write(requirements)


