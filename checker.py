# NarrativeIQ - checker.py
# Core NLP Quality Engine
# GVP Module VI + ICH E2B(R3) Compliance Checker
# Author: drbipinbhagath | License: MIT

import re
from synonyms import PV_SYNONYMS


class NarrativeChecker:
    """
    4-layer ICSR narrative quality checker:
    Layer 1: Rule-based regex keyword detection
    Layer 2: PV synonym expansion
    Layer 3: Seriousness criteria cross-check
    Layer 4: Semantic completeness scoring
    """

    def __init__(self):
        # GVP Module VI / ICH E2B(R3) mandatory narrative elements
        self.checklist = {
            "patient_demographics": {
                "label": "Patient Identifier / Demographics",
                "patterns": [
                    r"\d{1,3}[\s-]*year[s]?[\s-]*old",
                    r"\b(male|female|man|woman|boy|girl|infant|child|adult|elderly)\b",
                    r"\b(patient|subject|case|consumer|user|he|she)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.1",
                "ich_ref": "ICH E2B(R3) A.1"
            },
            "suspect_drug": {
                "label": "Suspect Drug Name and Details",
                "patterns": [
                    r"\b(administered|prescribed|received|started|initiated|taking|took|given)\b",
                    r"\b(tablet|capsule|injection|infusion|dose|mg|mcg|ml|patch|cream)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.4",
                "ich_ref": "ICH E2B(R3) B.4"
            },
            "adverse_event": {
                "label": "Adverse Event / Reaction Description",
                "patterns": [
                    r"\b(developed|experienced|presented|reported|suffered|showed|complained|onset)\b",
                    r"\b(reaction|event|effect|symptom|sign|condition|episode|complication)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.5",
                "ich_ref": "ICH E2B(R3) B.5"
            },
            "dose_route": {
                "label": "Dose and Route of Administration",
                "patterns": [
                    r"\b(oral|intravenous|subcutaneous|intramuscular|topical|inhaled|iv|sc|im|po)\b",
                    r"\b\d+\s*(mg|mcg|ml|g|iu|units?)\b",
                    r"\b(once|twice|three times|daily|weekly|bid|tid|qid|od)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.4",
                "ich_ref": "ICH E2B(R3) B.4.3"
            },
            "onset_date": {
                "label": "Date / Time of Event Onset",
                "patterns": [
                    r"\b(on|dated?|onset|started|began|first noted|approximately|around)\b.{0,30}(\d{4}|january|february|march|april|may|june|july|august|september|october|november|december)",
                    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
                    r"\b(day|week|month|hour)s?\b.{0,10}\b(after|following|post|later)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.5",
                "ich_ref": "ICH E2B(R3) B.5.2"
            },
            "outcome": {
                "label": "Event Outcome",
                "patterns": [
                    r"\b(recovered|recovering|resolved|resolution|improving|improved|ongoing|continuing)\b",
                    r"\b(fatal|death|died|deceased|sequelae|permanent|disability|hospitalised|hospitalised)\b",
                    r"\b(not recovered|unknown outcome|outcome unknown)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.6",
                "ich_ref": "ICH E2B(R3) B.5.8"
            },
            "causality": {
                "label": "Causality Assessment",
                "patterns": [
                    r"\b(possibly|probably|likely|unlikely|related|unrelated|causal|causality|assessed|considered)\b",
                    r"\b(WHO-UMC|naranjo|imputability|temporal relationship|dechallenge|rechallenge)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.7",
                "ich_ref": "ICH E2B(R3) B.5.9"
            },
            "reporter_details": {
                "label": "Reporter Type and Details",
                "patterns": [
                    r"\b(physician|doctor|nurse|pharmacist|patient|consumer|hcp|healthcare professional|reporter|investigator)\b",
                    r"\b(reported by|reported via|source|spontaneous|literature|study|clinical trial)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.2",
                "ich_ref": "ICH E2B(R3) A.2"
            },
            "seriousness": {
                "label": "Seriousness Criteria",
                "patterns": [
                    r"\b(serious|hospitalisation|hospitalised|life-threatening|death|congenital|disability|medically significant)\b",
                    r"\b(non-serious|non serious|mild|moderate|severe)\b"
                ],
                "gvp_ref": "GVP Module VI.A",
                "ich_ref": "ICH E2A"
            },
            "action_taken": {
                "label": "Action Taken with Drug",
                "patterns": [
                    r"\b(withdrawn|discontinued|stopped|reduced|dose reduced|interrupted|increased|not changed|unknown)\b",
                    r"\b(dechallenge|rechallenge|drug withdrawn)\b"
                ],
                "gvp_ref": "GVP Module VI.C.2.2.3.4",
                "ich_ref": "ICH E2B(R3) B.4.10"
            }
        }

        # Seriousness keywords for cross-check
        self.seriousness_flags = [
            r"\b(death|fatal|died|deceased)\b",
            r"\b(hospitalised|hospitalised|hospitalization|admitted)\b",
            r"\b(life-threatening|life threatening)\b",
            r"\b(disability|permanent damage|congenital anomaly|birth defect)\b",
            r"\b(medically significant|medically important)\b"
        ]

    def expand_with_synonyms(self, text):
        """Expand text with PV synonyms for better matching."""
        text_expanded = text.lower()
        for term, syns in PV_SYNONYMS.items():
            for syn in syns:
                if syn.lower() in text_expanded:
                    text_expanded += " " + term.lower()
                    break
        return text_expanded

    def check_seriousness_consistency(self, text_lower):
        """Check if seriousness criteria in text match the seriousness flag."""
        serious_markers_found = []
        for pattern in self.seriousness_flags:
            if re.search(pattern, text_lower):
                match = re.search(pattern, text_lower)
                serious_markers_found.append(match.group())
        return serious_markers_found

    def score_grade(self, score):
        """Assign a quality grade based on score."""
        if score >= 90:
            return "A", "Excellent - Submission Ready", "success"
        elif score >= 70:
            return "B", "Good - Minor Issues", "info"
        elif score >= 50:
            return "C", "Adequate - Requires QC", "warning"
        else:
            return "D", "Poor - Major Rework Needed", "danger"

    def check(self, text, product_name=None):
        """Run full quality check on narrative text."""
        results = {
            "overall_score": 0,
            "grade": "",
            "grade_label": "",
            "grade_class": "",
            "findings": [],
            "missing_elements": [],
            "warnings": [],
            "seriousness_markers": [],
            "total_checks": len(self.checklist),
            "passed_checks": 0,
            "failed_checks": 0
        }

        # Expand text with PV synonyms
        text_expanded = self.expand_with_synonyms(text)
        score_per_element = round(100 / len(self.checklist))
        score = 0

        # Layer 1 & 2: Rule-based + Synonym-expanded checks
        for key, rule in self.checklist.items():
            found = False
            for pattern in rule["patterns"]:
                if re.search(pattern, text_expanded, re.IGNORECASE):
                    found = True
                    break

            if found:
                score += score_per_element
                results["passed_checks"] += 1
                results["findings"].append({
                    "element": rule["label"],
                    "status": "Present",
                    "status_class": "success",
                    "gvp_ref": rule["gvp_ref"],
                    "ich_ref": rule["ich_ref"]
                })
            else:
                results["failed_checks"] += 1
                results["missing_elements"].append({
                    "element": rule["label"],
                    "status": "Missing",
                    "status_class": "danger",
                    "impact": "Required for GVP/ICH compliance",
                    "gvp_ref": rule["gvp_ref"],
                    "ich_ref": rule["ich_ref"]
                })

        # Layer 3: Product name verification
        if product_name and product_name.strip():
            pname = product_name.strip().upper()
            syns = PV_SYNONYMS.get(pname, [product_name.lower()])
            product_found = any(s.lower() in text_expanded for s in syns)
            if not product_found:
                results["warnings"].append(
                    f"Product name '{product_name}' or its synonyms not found in narrative text."
                )

        # Layer 4: Seriousness cross-check
        serious_markers = self.check_seriousness_consistency(text_expanded)
        if serious_markers:
            results["seriousness_markers"] = serious_markers
            results["warnings"].append(
                f"Seriousness markers detected: {', '.join(serious_markers)}. Verify seriousness box is ticked."
            )

        # Final score and grade
        results["overall_score"] = min(score, 100)
        grade, grade_label, grade_class = self.score_grade(results["overall_score"])
        results["grade"] = grade
        results["grade_label"] = grade_label
        results["grade_class"] = grade_class

        return results
