# NarrativeIQ - app.py
# Flask application entry point
# Author: drbipinbhagath
# License: MIT

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from checker import NarrativeChecker
from database import init_db, save_result, get_history

app = Flask(__name__)
app.secret_key = 'narrativeiq_secret_2024'

# Initialise database on startup
init_db()

# Initialise the NLP checker (loads PubMedBERT model)
checker = NarrativeChecker()


@app.route('/', methods=['GET'])
def index():
    """Home page - narrative input form."""
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_narrative():
    """Process submitted narrative and return QC results."""
    narrative_text = request.form.get('narrative', '').strip()
    case_id = request.form.get('case_id', 'CASE-001').strip()
    product_name = request.form.get('product_name', '').strip()

    if not narrative_text:
        return redirect(url_for('index'))

    # Run the quality check
    results = checker.check(narrative_text, product_name)

    # Save to audit history
    save_result(case_id, product_name, narrative_text, results)

    return render_template('results.html',
                           results=results,
                           narrative=narrative_text,
                           case_id=case_id,
                           product_name=product_name)


@app.route('/history', methods=['GET'])
def history():
    """Audit trail page showing all past QC checks."""
    records = get_history()
    return render_template('history.html', records=records)


@app.route('/api/check', methods=['POST'])
def api_check():
    """JSON API endpoint for programmatic access."""
    data = request.get_json()
    if not data or 'narrative' not in data:
        return jsonify({'error': 'No narrative provided'}), 400

    narrative_text = data['narrative']
    product_name = data.get('product_name', '')
    results = checker.check(narrative_text, product_name)
    return jsonify(results)


@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear audit history."""
    from database import clear_all
    clear_all()
    return redirect(url_for('history'))


if __name__ == '__main__':
    print("")
    print("========================================")
    print(" NarrativeIQ - ICSR Quality Checker")
    print(" Local AI-Powered PV Tool")
    print(" http://localhost:5000")
    print("========================================")
    print("")
    app.run(debug=False, host='127.0.0.1', port=5000)
