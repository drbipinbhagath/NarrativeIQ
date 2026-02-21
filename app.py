# NarrativeIQ - app.py
# Flask application entry point
# Author: drbipinbhagath (https://www.linkedin.com/in/drbipinchandrabhagath/)
# License: MIT

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
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
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    narrative = request.form.get('narrative', '').strip()
    case_id = request.form.get('case_id', 'CASE-001').strip()
    agency = request.form.get('agency', 'EMA').strip()
    
    if not narrative:
        return redirect(url_for('index'))
        
    # Run quality check
    results = checker.check_narrative(narrative, agency)
    
    # Save to database
    save_result(case_id, narrative, results['quality_score'], json.dumps(results['findings']))
    
    return render_template('results.html', 
                           results=results, 
                           narrative=narrative, 
                           case_id=case_id,
                           agency=agency)

@app.route('/dashboard')
def dashboard():
    history = get_history()
    return render_template('dashboard.html', history=history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
