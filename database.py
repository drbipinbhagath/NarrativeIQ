# NarrativeIQ - database.py
# SQLite Audit Trail Handler
# Author: drbipinbhagath | License: MIT

import sqlite3
import json
from datetime import datetime

DB_PATH = 'narrativeiq.db'


def get_connection():
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
            agency TEXT,
            narrative_text TEXT NOT NULL,
            overall_score INTEGER,
            grade TEXT,
            grade_label TEXT,
            passed_checks INTEGER,
            failed_checks INTEGER,
            total_checks INTEGER,
            checks_passed TEXT,
            checks_failed TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f'[NarrativeIQ] Database initialised at: {DB_PATH}')


def save_result(result):
    """Save a QC result to the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO qc_history (
                case_id, agency, narrative_text,
                overall_score, grade, grade_label,
                passed_checks, failed_checks, total_checks,
                checks_passed, checks_failed, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.get('case_id', 'UNKNOWN'),
            result.get('agency', 'EMA'),
            result.get('narrative', ''),
            result.get('score', 0),
            result.get('grade', 'F'),
            result.get('grade_label', ''),
            result.get('passed', 0),
            result.get('failed', 0),
            result.get('total', 0),
            json.dumps(result.get('checks_passed', [])),
            json.dumps(result.get('checks_failed', [])),
            result.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M'))
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'[Database] Error saving result: {e}')


def get_history():
    """Retrieve all QC history records."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM qc_history ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        records = []
        for row in rows:
            r = dict(row)
            # Parse JSON fields back to lists
            try:
                r['checks_passed'] = json.loads(r.get('checks_passed', '[]') or '[]')
            except Exception:
                r['checks_passed'] = []
            try:
                r['checks_failed'] = json.loads(r.get('checks_failed', '[]') or '[]')
            except Exception:
                r['checks_failed'] = []
            # Alias fields for template compatibility
            r['score'] = r.get('overall_score', 0)
            r['passed'] = r.get('passed_checks', 0)
            r['failed'] = r.get('failed_checks', 0)
            r['narrative'] = r.get('narrative_text', '')
            records.append(r)
        return records
    except Exception as e:
        print(f'[Database] Error fetching history: {e}')
        return []
