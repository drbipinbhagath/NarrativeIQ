# NarrativeIQ - database.py
# SQLite Audit Trail Handler
# Stores all QC checks with timestamps for inspection readiness
# Author: drbipinbhagath | License: MIT

import sqlite3
import json
from datetime import datetime

DB_PATH = 'narrativeiq.db'


def get_connection():
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialise the database and create tables if not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qc_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            product_name TEXT,
            narrative_text TEXT NOT NULL,
            overall_score INTEGER,
            grade TEXT,
            grade_label TEXT,
            passed_checks INTEGER,
            failed_checks INTEGER,
            total_checks INTEGER,
            findings_json TEXT,
            missing_json TEXT,
            warnings_json TEXT,
            checked_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("[NarrativeIQ] Database initialised at:", DB_PATH)


def save_result(case_id, product_name, narrative_text, results):
    """Save a QC check result to the audit trail."""
    conn = get_connection()
    cursor = conn.cursor()

    checked_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO qc_history (
            case_id, product_name, narrative_text,
            overall_score, grade, grade_label,
            passed_checks, failed_checks, total_checks,
            findings_json, missing_json, warnings_json,
            checked_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        case_id,
        product_name or '',
        narrative_text,
        results.get('overall_score', 0),
        results.get('grade', ''),
        results.get('grade_label', ''),
        results.get('passed_checks', 0),
        results.get('failed_checks', 0),
        results.get('total_checks', 0),
        json.dumps(results.get('findings', [])),
        json.dumps(results.get('missing_elements', [])),
        json.dumps(results.get('warnings', [])),
        checked_at
    ))

    conn.commit()
    conn.close()


def get_history(limit=100):
    """Retrieve QC history records for audit trail display."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, case_id, product_name, overall_score,
               grade, grade_label, passed_checks, failed_checks,
               total_checks, checked_at
        FROM qc_history
        ORDER BY checked_at DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            'id': row['id'],
            'case_id': row['case_id'],
            'product_name': row['product_name'],
            'overall_score': row['overall_score'],
            'grade': row['grade'],
            'grade_label': row['grade_label'],
            'passed_checks': row['passed_checks'],
            'failed_checks': row['failed_checks'],
            'total_checks': row['total_checks'],
            'checked_at': row['checked_at'],
            'grade_class': get_grade_class(row['grade'])
        })

    return history


def get_record_by_id(record_id):
    """Get a single QC record with full details by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM qc_history WHERE id = ?', (record_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'id': row['id'],
            'case_id': row['case_id'],
            'product_name': row['product_name'],
            'narrative_text': row['narrative_text'],
            'overall_score': row['overall_score'],
            'grade': row['grade'],
            'grade_label': row['grade_label'],
            'passed_checks': row['passed_checks'],
            'failed_checks': row['failed_checks'],
            'total_checks': row['total_checks'],
            'findings': json.loads(row['findings_json'] or '[]'),
            'missing_elements': json.loads(row['missing_json'] or '[]'),
            'warnings': json.loads(row['warnings_json'] or '[]'),
            'checked_at': row['checked_at'],
            'grade_class': get_grade_class(row['grade'])
        }
    return None


def clear_all():
    """Clear all audit history records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM qc_history')
    conn.commit()
    conn.close()


def get_stats():
    """Get summary statistics for dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM qc_history')
    total = cursor.fetchone()['total']

    cursor.execute('SELECT AVG(overall_score) as avg_score FROM qc_history')
    avg = cursor.fetchone()['avg_score']

    cursor.execute(
        'SELECT COUNT(*) as count FROM qc_history WHERE overall_score >= 70'
    )
    passed = cursor.fetchone()['count']

    conn.close()

    return {
        'total_checks': total,
        'average_score': round(avg or 0, 1),
        'passed_count': passed,
        'failed_count': total - passed
    }


def get_grade_class(grade):
    """Return Bootstrap badge class for a grade."""
    mapping = {
        'A': 'success',
        'B': 'info',
        'C': 'warning',
        'D': 'danger'
    }
    return mapping.get(grade, 'secondary')
