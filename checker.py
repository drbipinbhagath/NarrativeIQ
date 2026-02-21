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
        # Each element: keywords (whole-word regex), GVP ref, ICH ref, impact if missing
        self.checklist = [
            {
                'element': 'Patient Demographics',
                'keywords': [
                    r'\byear[s]?\s+old\b', r'\baged?\b', r'\bmale\b', r'\bfemale\b',
                    r'\bman\b', r'\bwoman\b', r'\bboy\b', r'\bgirl\b',
                    r'\bpatient\b', r'\bsubject\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.1',
                'ich_ref': 'E2B(R3) A.1',
                'impact': 'Cannot assess patient-specific risk factors'
            },
            {
                'element': 'Suspect Drug',
                'keywords': [
                    r'\bsuspect\b', r'\bsuspected\b', r'\bcausative\b',
                    r'\btreated with\b', r'\bprescribed\b', r'\bmedication\b',
                    r'\bdrug\b', r'\btherapy\b', r'\btreatment\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.2',
                'ich_ref': 'E2B(R3) G.k',
                'impact': 'Cannot identify the implicated medicinal product'
            },
            {
                'element': 'Indication for Use',
                'keywords': [
                    r'\bindication\b', r'\bprescribed for\b', r'\btreated for\b',
                    r'\bdiagnosed with\b', r'\bsuffering from\b', r'\bmanagement of\b',
                    r'\bfor the treatment\b', r'\bfor\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.2',
                'ich_ref': 'E2B(R3) G.k.7',
                'impact': 'Unable to evaluate appropriateness of drug use'
            },
            {
                'element': 'Dose and Route',
                'keywords': [
                    r'\bmg\b', r'\bml\b', r'\bmcg\b', r'\bmicrogram\b',
                    r'\boral\b', r'\bintravenous\b', r'\biv\b', r'\bsc\b',
                    r'\bsubcutaneous\b', r'\bintramuscular\b', r'\bim\b',
                    r'\bdose\b', r'\bdosage\b', r'\broute\b', r'\badministered\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.2',
                'ich_ref': 'E2B(R3) G.k.4',
                'impact': 'Cannot perform dose-response analysis'
            },
            {
                'element': 'Dates of Drug Use',
                'keywords': [
                    r'\bstarted\b', r'\binitiated\b', r'\bbegun\b', r'\bbegan\b',
                    r'\bdiscontinued\b', r'\bstopped\b', r'\bcessation\b',
                    r'\bdate\b', r'\bsince\b', r'\bfrom\b', r'\buntil\b',
                    r'\bfor\s+\d+\s+day', r'\bfor\s+\d+\s+week',
                    r'\bfor\s+\d+\s+month'
                ],
                'gvp_ref': 'GVP VI.B.5.3.2',
                'ich_ref': 'E2B(R3) G.k.4.r.1',
                'impact': 'Cannot establish temporal relationship'
            },
            {
                'element': 'Adverse Event Description',
                'keywords': [
                    r'\bexperienced\b', r'\bdeveloped\b', r'\bpresented\b',
                    r'\bcomplained\b', r'\breported\b', r'\bnoticed\b',
                    r'\badverse\b', r'\breaction\b', r'\bevent\b', r'\bsymptom\b',
                    r'\bside effect\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.3',
                'ich_ref': 'E2B(R3) E.i',
                'impact': 'Core safety event not described'
            },
            {
                'element': 'Seriousness Criteria',
                'keywords': [
                    r'\bserious\b',
                    r'\bnon-serious\b',
                    r'\bhospitali[sz]ed\b',
                    r'\bhospitali[sz]ation\b',
                    r'\blife.threatening\b',
                    r'\bfatal\b',
                    r'\bdeath\b',
                    r'\bdied\b',
                    r'\bdisabling\b',
                    r'\bdisability\b',
                    r'\bcongenital\b',
                    r'\bmedically significant\b',
                    r'\bsignificant disability\b',
                    r'\bpermanent damage\b',
                    r'\bicu\b',
                    r'\bcritical\b',
                    r'\bemergency\b'
                ],
                'gvp_ref': 'GVP VI.B.1',
                'ich_ref': 'E2B(R3) E.i.3.2',
                'impact': 'Regulatory seriousness classification incomplete'
            },
            {
                'element': 'Outcome',
                'keywords': [
                    r'\brecovered\b', r'\brecovering\b', r'\bresolved\b',
                    r'\bimproved\b', r'\bpersisting\b', r'\bongoing\b',
                    r'\bfatal\b', r'\bdeceased\b', r'\bunknown outcome\b',
                    r'\boutcome\b', r'\bsequelae\b', r'\bnot recovered\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.3',
                'ich_ref': 'E2B(R3) E.i.7',
                'impact': 'Cannot assess clinical resolution or prognosis'
            },
            {
                'element': 'Causality Assessment',
                'keywords': [
                    r'\bcausality\b', r'\bcausal\b', r'\brelated\b',
                    r'\bunrelated\b', r'\bpossibly\b', r'\bprobably\b',
                    r'\blikely\b', r'\bunlikely\b', r'\bcertain\b',
                    r'\bnot assessable\b', r'\bnot related\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.4',
                'ich_ref': 'E2B(R3) H.1',
                'impact': 'Benefit-risk evaluation incomplete without causality'
            },
            {
                'element': 'Dechallenge / Rechallenge',
                'keywords': [
                    r'\bdechallenge\b', r'\brechallenge\b',
                    r'\bwithdraw[n]?\b', r'\bwithdrawal\b',
                    r'\bdrug\s+stopped\b', r'\bdrug\s+discontinued\b',
                    r'\bsymptoms\s+resolved\b', r'\bsymptoms\s+improved\b',
                    r'\breintroduc\b', r'\bworsened\s+on\s+restarting\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.4',
                'ich_ref': 'E2B(R3) G.k.8',
                'impact': 'Causality signal strengthening data missing'
            },
            {
                'element': 'Relevant Medical History',
                'keywords': [
                    r'\bmedical history\b', r'\bhistory of\b', r'\bpast history\b',
                    r'\bprevious\b', r'\bcomorbid\b', r'\bcomorbidities\b',
                    r'\bno relevant\b', r'\bno significant history\b',
                    r'\bno known\b', r'\bbackground\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.1',
                'ich_ref': 'E2B(R3) D.7',
                'impact': 'Confounding factors cannot be excluded'
            },
            {
                'element': 'Concomitant Medications',
                'keywords': [
                    r'\bconcomitant\b', r'\bconcomitant medication\b',
                    r'\bco-medication\b', r'\bother medication\b',
                    r'\bno other medication\b', r'\bno concomitant\b',
                    r'\bconcomitant drug\b', r'\bco-administered\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.1',
                'ich_ref': 'E2B(R3) G.k.9',
                'impact': 'Drug interaction assessment incomplete'
            },
            {
                'element': 'Reporter Information',
                'keywords': [
                    r'\breported by\b', r'\breporter\b', r'\bphysician\b',
                    r'\bdoctor\b', r'\bnurse\b', r'\bpharmacist\b',
                    r'\bpatient reported\b', r'\bspontaneous\b',
                    r'\bliterature\b', r'\bstudy\b'
                ],
                'gvp_ref': 'GVP VI.B.5.3.5',
                'ich_ref': 'E2B(R3) C.2',
                'impact': 'Source credibility cannot be assessed'
            }
        ]

    def _check_element(self, narrative_lower, keywords):
        """Check if ANY keyword pattern matches using whole-word boundaries."""
        for pattern in keywords:
            if re.search(pattern, narrative_lower, re.IGNORECASE):
                return True
        return False

    def check(self, narrative, case_id=None, agency='EMA'):
        """Run all checklist items against narrative and return scored result."""
        if not case_id:
            case_id = str(uuid.uuid4())[:8].upper()

        narrative_lower = narrative.lower()

        passed = []
        failed = []
        checks_passed = []
        checks_failed = []

        for item in self.checklist:
            found = self._check_element(narrative_lower, item['keywords'])

            check_record = {
                'element': item['element'],
                'gvp_ref': item['gvp_ref'],
                'ich_ref': item['ich_ref'],
                'impact': item['impact'],
                'status': 'PASS' if found else 'FAIL'
            }

            if found:
                passed.append(item['element'])
                checks_passed.append(check_record)
            else:
                failed.append(item['element'])
                checks_failed.append(check_record)

        total = len(self.checklist)
        score = round((len(passed) / total) * 100, 1) if total > 0 else 0

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
