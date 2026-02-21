# NarrativeIQ

> **Local AI-powered ICSR Narrative Quality Checker for Pharmacovigilance Professionals**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GVP Module VI](https://img.shields.io/badge/GVP-Module%20VI%20Compliant-orange)](https://www.ema.europa.eu)
[![Offline](https://img.shields.io/badge/Mode-100%25%20Offline-red)]()

---

## Overview

**NarrativeIQ** is a desktop web application that uses AI (PubMedBERT) to automatically check the quality of Individual Case Safety Report (ICSR) narratives. Designed specifically for pharmacovigilance professionals, it runs **100% locally** — no internet required, no data leaves your machine.

Built with the same philosophy as modern PV automation tools, NarrativeIQ bridges the gap between manual narrative review and AI-assisted quality assurance.

---

## Key Features

- **AI-Powered Analysis** — Uses PubMedBERT (sentence-transformers) for semantic narrative understanding
- **GVP Module VI Compliance** — Checks against EMA Good Pharmacovigilance Practices Module VI criteria
- **ICH E2B Element Coverage** — Validates presence of mandatory ICSR data elements
- **MedDRA Terminology Check** — Flags non-standard medical terminology
- **Multi-Agency Support** — Covers EMA, FDA, PMDA, Health Canada narrative standards
- **Quality Score** — Generates an overall narrative quality score (0–100)
- **Detailed Feedback** — Section-by-section improvement suggestions
- **History Tracking** — SQLite database stores all checked narratives
- **Export Ready** — Copy results for reports or QC documentation
- **100% Offline** — No API calls, no cloud dependency, GDPR-safe

---

## Repository Structure

```
NarrativeIQ/
├── app.py                  # Flask web application (main entry point)
├── checker.py              # Core AI narrative quality checking engine
├── synonyms.py             # Medical terminology & MedDRA synonym mapper
├── database.py             # SQLite database handler (history & storage)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html          # Main input page (narrative submission)
│   ├── results.html        # Quality check results display
│   └── history.html        # Past checks history viewer
├── static/
│   └── style.css           # UI styling (clean, professional)
├── README.md               # This file
└── LICENSE                 # MIT License
```

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- 4 GB RAM minimum (for PubMedBERT model)
- ~2 GB disk space (for AI model download on first run)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/drbipinbhagath/NarrativeIQ.git
cd NarrativeIQ
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

> Note: The first run will download the PubMedBERT model (~420 MB). This happens once and is cached locally.

**4. Run the application**
```bash
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## Usage Guide

### Step 1 — Paste Your Narrative
Navigate to the home page and paste your ICSR narrative text into the input box.

### Step 2 — Select Agency (Optional)
Choose the target regulatory agency:
- **EMA** (default) — European Medicines Agency
- **FDA** — US Food and Drug Administration
- **PMDA** — Japanese Pharmaceuticals and Medical Devices Agency
- **Health Canada**

### Step 3 — Run Quality Check
Click **"Check Narrative Quality"** to start the AI analysis.

### Step 4 — Review Results
The results page shows:
- **Overall Quality Score** (0–100)
- **Section Scores** for each narrative component
- **Missing Elements** flagged with GVP VI references
- **Improvement Suggestions** with specific guidance
- **Terminology Flags** for non-MedDRA terms detected

### Step 5 — History
All checked narratives are saved locally. Access previous results via the **History** tab.

---

## Quality Check Criteria

NarrativeIQ evaluates narratives against the following standard elements:

| Element | GVP VI Reference | ICH E2B Field |
|---|---|---|
| Patient demographics | Section B.4 | D.1–D.3 |
| Suspect drug(s) | Section B.4 | G.k |
| Indication for use | Section B.4 | G.k.7 |
| Adverse event description | Section B.4 | E.i |
| Onset date / timeline | Section B.4 | E.i.4 |
| Dechallenge / rechallenge | Section B.4 | G.k.8–9 |
| Outcome at data lock | Section B.4 | E.i.7 |
| Reporter information | Section B.1 | C.1–C.3 |
| Causality assessment | Section B.4 | H.1 |
| Medical history | Section B.4 | D.7–D.8 |

---

## Technology Stack

| Component | Technology |
|---|---|
| Web Framework | Flask 2.3+ |
| AI Model | PubMedBERT (sentence-transformers) |
| Deep Learning | PyTorch 2.0+ |
| Database | SQLite (built-in Python) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Config Management | python-dotenv |
| Testing | pytest, pytest-flask |

---

## Compliance & Standards

- **EMA GVP Module VI** — Good Pharmacovigilance Practices (Revision 2)
- **ICH E2B(R3)** — Electronic transmission of individual case safety reports
- **ICH E2A** — Clinical safety data management definitions
- **MedDRA 26.1** — Medical Dictionary for Regulatory Activities
- **GDPR Compliant** — All data stays on local machine, zero external transmission

---

## Limitations

- NarrativeIQ is a **quality assistance tool**, not a replacement for qualified PV review
- MedDRA synonym coverage is representative, not exhaustive (full MedDRA license required for production use)
- AI scoring is indicative — regulatory submission decisions must involve trained pharmacovigilance personnel
- First-run model download requires internet; subsequent runs are fully offline

---

## Roadmap

- [ ] PDF/Word narrative import
- [ ] Batch processing (multiple narratives)
- [ ] E2B(R3) XML field mapping export
- [ ] Custom agency rule configuration
- [ ] Docker containerisation
- [ ] Integration with Argus/ARISg via API

---

## Contributing

Contributions are welcome! Please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Author

**Dr. Bipin Bhagath**  
Senior Pharmacovigilance Physician | AI in PV Enthusiast  
GitHub: [@drbipinbhagath](https://github.com/drbipinbhagath)

---

## Disclaimer

This tool is intended for educational and quality improvement purposes within pharmacovigilance workflows. It does not constitute regulatory or legal advice. Always follow your organisation's SOPs and applicable regulatory guidelines for ICSR processing and submission.
