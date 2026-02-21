# NarrativeIQ - checker.py
# Core ICSR Narrative Quality Engine
# GVP Module VI + ICH E2B(R3) Rule-Based Checker
# Author: drbipinbhagath | License: MIT

import re
import uuid
from datetime import datetime


class NarrativeChecker:
    """
    Rule-based ICSR narrative quality checker.
    Checks against GVP Module VI and ICH E2B(R3) mandatory elements.
    Returns a standardised result dict compatible with all templates.
    """

    def __init__(self):
        # Each element: keywords, GVP ref, ICH ref, impact if missing
        self.checklist = [
            {
                'element': 'Patient Demographics',
                'keywords': ['year', 'years old', 'age', 'male', 'female', 'patient', 'man', 'woman', 'boy', 'girl', 'child', 'adult', 'elderly'],
                'gvp_ref': 'GVP VI.C.2.2.3.1',
                'ich_ref': 'E2B(R3) D.1-D.3',
                'impact': 'Cannot identify reporter or patient'
            },
            {
                'element': 'Suspect Drug Name',
                'keywords': ['prescribed', 'administered', 'drug', 'medication', 'medicine', 'tablet', 'capsule', 'injection', 'dose', 'mg', 'treatment', 'therapy', 'took', 'received', 'given'],
                'gvp_ref': 'GVP VI.C.2.2.3.4',
                'ich_ref': 'E2B(R3) G.k.2.2',
                'impact': 'Suspect drug cannot be identified'
            },
            {
                'element': 'Indication for Use',
                'keywords': ['for', 'indication', 'treating', 'treatment of', 'diagnosed', 'diagnosis', 'condition', 'disease', 'disorder', 'diabetes', 'hypertension', 'infection', 'pain', 'cancer', 'prescribed for'],
                'gvp_ref': 'GVP VI.C.2.2.3.4',
                'ich_ref': 'E2B(R3) G.k.7',
                'impact': 'Clinical context incomplete'
            },
            {
                'element': 'Adverse Event Description',
                'keywords': ['developed', 'experienced', 'reported', 'complained', 'presented', 'suffered', 'reaction', 'event', 'symptom', 'nausea', 'vomiting', 'rash', 'pain', 'fever', 'dizziness', 'fatigue', 'headache', 'adverse', 'side effect', 'injury'],
                'gvp_ref': 'GVP VI.C.2.2.3.5',
                'ich_ref': 'E2B(R3) E.i.1',
                'impact': 'Adverse event not described'
            },
            {
                'element': 'Onset Date / Timeline',
                'keywords': ['on ', 'after', 'day', 'days', 'week', 'weeks', 'month', 'months', 'hours', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', '2024', '2025', '2026', 'initiation', 'started', 'began', 'following'],
                'gvp_ref': 'GVP VI.C.2.2.3.5',
                'ich_ref': 'E2B(R3) E.i.4',
                'impact': 'Cannot establish temporal relationship'
            },
            {
                'element': 'Seriousness Criteria',
                'keywords': ['serious', 'hospitalisation', 'hospitalized', 'hospitalised', 'life-threatening', 'death', 'died', 'disability', 'medically significant', 'non-serious', 'not serious', 'recovered', 'congenital'],
                'gvp_ref': 'GVP VI.A',
                'ich_ref': 'E2B(R3) A.1.5',
                'impact': 'Seriousness classification missing'
            },
            {
                'element': 'Action Taken with Drug',
                'keywords': ['withdrawn', 'discontinued', 'stopped', 'reduced', 'dose reduced', 'continued', 'not changed', 'drug withdrawn', 'drug stopped', 'rechallenge', 'dechallenge'],
                'gvp_ref': 'GVP VI.C.2.2.3.4',
                'ich_ref': 'E2B(R3) G.k.8',
                'impact': 'Drug management unclear'
            },
            {
                'element': 'Outcome of Event',
                'keywords': ['recovered', 'recovering', 'resolved', 'resolving', 'fatal', 'died', 'death', 'ongoing', 'not recovered', 'sequelae', 'unknown', 'improved', 'worsened', 'outcome'],
                'gvp_ref': 'GVP VI.C.2.2.3.6',
                'ich_ref': 'E2B(R3) E.i.7',
                'impact': 'Case outcome not documented'
            },
            {
                'element': 'Causality Assessment',
                'keywords': ['related', 'possibly related', 'probably related', 'unlikely', 'unrelated', 'causal', 'causality', 'assessed', 'considered', 'association', 'temporal'],
                'gvp_ref': 'GVP VI.C.2.2.3.7',
                'ich_ref': 'E2B(R3) H.1',
                'impact': 'Causality not assessed'
            },
            {
                'element': 'Reporter Information',
                'keywords': ['reported by', 'reporter', 'physician', 'doctor', 'nurse', 'pharmacist', 'healthcare professional', 'consumer', 'patient reported', 'report received', 'spontaneous'],
                'gvp_ref': 'GVP VI.C.2.2.2',
                'ich_ref': 'E2B(R3) C.1-C.3',
                'impact': 'Reporter qualification unknown'
            },
        ]

    def check(self, narrative, case_id=None, agency='EMA'):
        """
        Run quality check on narrative text.
        Returns a standardised result dictionary.
        """
        if not case_id:
            case_id = 'NIQ-' + str(uuid.uuid4())[:8].upper()

        text = narrative.lower()
        checks_passed = []
        checks_failed = []

        for item in self.checklist:
            found = any(kw.lower() in text for kw in item['keywords'])
            entry = {
                'element': item['element'],
                'gvp_ref': item['gvp_ref'],
                'ich_ref': item['ich_ref'],
                'impact': item['impact'],
                'found': found
            }
            if found:
                checks_passed.append(entry)
            else:
                checks_failed.append(entry)

        total = len(self.checklist)
        passed = len(checks_passed)
        failed = len(checks_failed)
        score = round((passed / total) * 100)

        # Grade assignment
        if score >= 90:
            grade = 'A'
            grade_label = 'Submission Ready'
        elif score >= 75:
            grade = 'B'
            grade_label = 'Minor Revisions Needed'
        elif score >= 60:
            grade = 'C'
            grade_label = 'Significant Revisions Needed'
        else:
            grade = 'F'
            grade_label = 'Major Rework Required'

        result = {
            'case_id': case_id,
            'agency': agency,
            'narrative': narrative,
            'score': score,
            'grade': grade,
            'grade_label': grade_label,
            'passed': passed,
            'failed': failed,
            'total': total,
            'checks_passed': checks_passed,
            'checks_failed': checks_failed,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        }

        return result
