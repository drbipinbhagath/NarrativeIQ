# NarrativeIQ

> **Local AI-powered ICSR Narrative Quality Checker for Pharmacovigilance Professionals**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GVP Module VI](https://img.shields.io/badge/GVP-Module%20VI%20Compliant-orange)](https://www.ema.europa.eu)
[![Offline](https://img.shields.io/badge/Mode-100%25%20Offline-red)]()

---

## Overview

**NarrativeIQ** is a desktop web application that uses AI (PubMedBERT) to automatically check the quality of Individual Case Safety Report (ICSR) narratives. Designed specifically for pharmacovigilance professionals, it runs **100% locally** – no internet required, no data leaves your machine.

Built with the same philosophy as modern PV automation tools, NarrativeIQ bridges the gap between manual narrative review and AI-assisted quality assurance.

## Features

- **Automated Quality Checks**: Validates narratives against GVP Module VI and ICH E2B(R3) mandatory elements.
- **PubMedBERT Integration**: Uses a domain-specific transformer model trained on biomedical literature for high accuracy.
- **Interactive Dashboard**: Track your QC performance, scores, and common errors over time.
- **Audit History**: Maintains a local SQLite database of all performed checks for internal review.
- **Privacy by Design**: Runs entirely on your local machine. Ideal for sensitive clinical data.

## Quality Elements Checked

NarrativeIQ evaluates each narrative for 10 mandatory clinical elements:

1. **Patient Demographics** (Age, Gender)
2. **Suspect Drug Details** (Name, Indication)
3. **Adverse Event Description**
4. **Dose and Route**
5. **Onset Date / Time**
6. **Event Outcome**
7. **Causality Assessment**
8. **Reporter Information**
9. **Seriousness Criteria**
10. **Action Taken with Drug**

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/drbipinbhagath/NarrativeIQ.git
   cd NarrativeIQ
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the tool:
   Open your browser and navigate to `http://localhost:5000`

## Contributing

Contributions are welcome! If you have suggestions for new quality rules or PV-specific features:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Author
**Dr Bipin Chandra Bhagath** - *Senior PV Physician-AI & Technology Projects*  
[LinkedIn Profile](https://www.linkedin.com/in/drbipinchandrabhagath/)
