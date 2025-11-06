# 🧾 Booking Netto — Backend Skeleton

Backend minimale in **Python (FastAPI)** per analizzare PDF provenienti da **Booking.com** e da **fatture**, estrarre importi e calcolare l’**incasso netto** a partire dal lordo, applicando **commissioni**, **IVA** e **tasse di soggiorno** definite in un file di configurazione.

> 🔧 Tecnologie usate: FastAPI, invoice2data, pdfplumber, Pandas, Pydantic, YAML

---

## 🚀 Obiettivo del progetto

Questo backend permette di:
- Caricare PDF tramite API (`/analyze`);
- Estrarre automaticamente i valori principali (lordo, commissione, payout, notti, ospiti);
- Applicare regole di calcolo definite in `rules.yaml`;
- Restituire un output JSON con l’**incasso netto** e un **breakdown dettagliato**.

L’idea è creare un sistema **deterministico** (senza modelli AI), stabile, veloce e adatto a file ripetitivi come report Booking e fatture standardizzate.

---

## 🧠 Tecniche e librerie utilizzate

| Funzione | Libreria / Strumento | Descrizione |
|-----------|----------------------|--------------|
| **API backend** | `FastAPI` | Framework web veloce e moderno per esporre endpoint REST |
| **Parsing PDF (fatture / report)** | `invoice2data` | Estrae dati tramite template YAML con regex dedicate |
| **Fallback OCR/Text** | `pdfplumber` | Estrae testo leggibile dai PDF quando i template non trovano match |
| **Analisi e calcolo** | `pandas`, `pydantic` | Pydantic valida i dati, Pandas (opzionale) per aggregazioni future |
| **Configurazioni** | `PyYAML` | Regole di calcolo personalizzabili (IVA, commissioni, tasse, ecc.) |
| **Template regex** | `YAML` templates in `app/extractors/invoice2data_templates` | Definiscono come riconoscere importi e campi nei PDF |
| **Gestione ambienti** | `venv` | Ambiente virtuale Python per isolamento del progetto |

---

## 📁 Struttura del progetto

