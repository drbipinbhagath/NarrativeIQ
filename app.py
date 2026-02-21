# NarrativeIQ - app.py
# Flask application entry point
# Author: drbipinbhagath
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
    result = checker.check(narrative, case_id=case_id, agency=agency)

    # Save to database
    save_result(result)

    return render_template('results.html', result=result)


@app.route('/history')
def history():
    records = get_history()
    return render_template('history.html', records=records)


@app.route('/dashboard')
def dashboard():
    import sqlite3
    from collections import Counter

    db_path = 'narrativeiq.db'
    recent_cases = []
    stats = {'total_cases': 0, 'avg_score': 0, 'grade_a_count': 0, 'fail_count': 0}
    trend_labels, trend_scores = [], []
    grade_labels, grade_counts = [], []
    missing_labels, missing_counts = [], []
    hist_data = [0, 0, 0, 0, 0]

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Use correct table name: qc_history
        cur.execute("SELECT * FROM qc_history ORDER BY id DESC LIMIT 20")
        rows = cur.fetchall()
        recent_cases = [dict(r) for r in rows]

        if recent_cases:
            # Use correct field names from qc_history table
            scores = [r.get('overall_score', 0) for r in recent_cases]
            stats['total_cases'] = len(recent_cases)
            stats['avg_score'] = round(sum(scores) / len(scores), 1)
            stats['grade_a_count'] = sum(1 for r in recent_cases if r.get('grade') == 'A')
            stats['fail_count'] = sum(1 for r in recent_cases if r.get('overall_score', 100) < 60)

            # Score trend (oldest to newest)
            ordered = list(reversed(recent_cases))
            trend_labels = [r.get('case_id', '') for r in ordered]
            trend_scores = [r.get('overall_score', 0) for r in ordered]

            # Grade distribution
            grade_counter = Counter(r.get('grade', 'N/A') for r in recent_cases)
            grade_labels = list(grade_counter.keys())
            grade_counts = list(grade_counter.values())

            # Score histogram
            for s in scores:
                if s <= 20: hist_data[0] += 1
                elif s <= 40: hist_data[1] += 1
                elif s <= 60: hist_data[2] += 1
                elif s <= 80: hist_data[3] += 1
                else: hist_data[4] += 1

            # Most frequently missing elements
            all_missing = []
            for r in recent_cases:
                try:
                    failed_raw = r.get('failed_elements', '[]') or '[]'
                    failed = json.loads(failed_raw)
                    if isinstance(failed, list):
                        for item in failed:
                            if isinstance(item, dict):
                                all_missing.append(item.get('element', str(item)))
                            else:
                                all_missing.append(str(item))
                except Exception:
                    pass
            missing_counter = Counter(all_missing).most_common(8)
            missing_labels = [m[0] for m in missing_counter]
            missing_counts = [m[1] for m in missing_counter]

            # Map field names for template compatibility
            for r in recent_cases:
                r['score'] = r.get('overall_score', 0)
                r['passed'] = r.get('passed_checks', 0)
                r['failed'] = r.get('failed_checks', 0)
                r['created_at'] = r.get('created_at', '')

        conn.close()
    except Exception as e:
        print(f'[Dashboard] Error: {e}')
        import traceback
        traceback.print_exc()

    return render_template(
        'dashboard.html',
        stats=stats,
        recent_cases=recent_cases,
        trend_labels=trend_labels,
        trend_scores=trend_scores,
        grade_labels=grade_labels,
        grade_counts=grade_counts,
        missing_labels=missing_labels,
        missing_counts=missing_counts,
        hist_data=hist_data
    )


@app.route('/api/history')
def api_history():
    records = get_history()
    return jsonify(records)


if __name__ == '__main__':
    print('\n' + '='*40)
    print(' NarrativeIQ - ICSR Quality Checker')
    print(' Local AI-Powered PV Tool')
    print(' http://localhost:5000')
    print('='*40 + '\n')
    app.run(debug=False, host='0.0.0.0', port=5000)
