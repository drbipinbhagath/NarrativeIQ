# NarrativeIQ - synonyms.py
# PV Terminology Synonym Dictionary
# Maps regulatory acronyms, report types, agency names, MedDRA terms
# Author: drbipinbhagath | License: MIT

# Master PV synonym dictionary
# Key = canonical term | Value = list of accepted synonyms/aliases
PV_SYNONYMS = {

    # ── Report Types ──────────────────────────────────────────────────────────
    "PSUR": [
        "periodic safety update report",
        "pbrer",
        "periodic benefit-risk evaluation report",
        "periodic benefit risk evaluation report",
        "aggregate safety report",
        "periodic report"
    ],
    "PBRER": [
        "psur",
        "periodic safety update report",
        "periodic benefit-risk evaluation report",
        "periodic benefit risk evaluation report"
    ],
    "ICSR": [
        "individual case safety report",
        "case report",
        "adverse event report",
        "adr report",
        "spontaneous report",
        "medwatch",
        "yellow card",
        "cioms form",
        "cioms i"
    ],
    "DSUR": [
        "development safety update report",
        "annual safety report",
        "asr",
        "investigational drug safety report"
    ],
    "RMP": [
        "risk management plan",
        "risk minimisation",
        "risk minimization",
        "rems",
        "risk evaluation and mitigation strategy"
    ],
    "SUSAR": [
        "suspected unexpected serious adverse reaction",
        "unexpected serious adverse reaction",
        "unexpected sar"
    ],
    "SAR": [
        "serious adverse reaction",
        "serious adr",
        "serious adverse drug reaction"
    ],
    "SAE": [
        "serious adverse event",
        "serious ae",
        "serious event"
    ],
    "AESI": [
        "adverse event of special interest",
        "special interest adverse event",
        "event of special interest"
    ],

    # ── Regulatory Agencies ───────────────────────────────────────────────────
    "EMA": [
        "european medicines agency",
        "european medicine agency",
        "emea"
    ],
    "FDA": [
        "food and drug administration",
        "us fda",
        "usfda",
        "u.s. food and drug administration"
    ],
    "MHRA": [
        "medicines and healthcare products regulatory agency",
        "uk mhra",
        "uk regulator"
    ],
    "PMDA": [
        "pharmaceuticals and medical devices agency",
        "japan pmda",
        "japanese agency"
    ],
    "CDSCO": [
        "central drugs standard control organisation",
        "india cdsco",
        "indian regulator",
        "dcgi"
    ],
    "TGA": [
        "therapeutic goods administration",
        "australia tga",
        "australian regulator"
    ],
    "HEALTH_CANADA": [
        "health canada",
        "canada health",
        "hc"
    ],

    # ── PV Guidelines & Modules ───────────────────────────────────────────────
    "GVP": [
        "good pharmacovigilance practice",
        "good pharmacovigilance practices",
        "guideline on good pharmacovigilance"
    ],
    "ICH_E2A": [
        "ich e2a",
        "clinical safety data management",
        "definitions for expedited reporting"
    ],
    "ICH_E2B": [
        "ich e2b",
        "electronic transmission of individual case safety reports",
        "e2b(r3)",
        "e2b r3"
    ],
    "ICH_E2C": [
        "ich e2c",
        "periodic benefit-risk evaluation",
        "e2c(r2)",
        "e2c r2"
    ],
    "ICH_E2D": [
        "ich e2d",
        "post-approval safety data management",
        "expedited reporting post-approval"
    ],
    "ICH_E2E": [
        "ich e2e",
        "pharmacovigilance planning",
        "pvp"
    ],

    # ── Case Classification & Coding ──────────────────────────────────────────
    "MEDDRA": [
        "medical dictionary for regulatory activities",
        "meddra coding",
        "medical dictionary regulatory"
    ],
    "PT": [
        "preferred term",
        "meddra pt",
        "preferred meddra term"
    ],
    "LLT": [
        "lowest level term",
        "meddra llt",
        "lowest level meddra term"
    ],
    "SOC": [
        "system organ class",
        "meddra soc",
        "organ class"
    ],
    "WHO_DD": [
        "who drug dictionary",
        "who-dd",
        "who drug",
        "who drug coding"
    ],

    # ── Causality Terms ───────────────────────────────────────────────────────
    "CAUSALITY": [
        "causal relationship",
        "causality assessment",
        "imputability",
        "temporal relationship",
        "cause and effect"
    ],
    "DECHALLENGE": [
        "drug withdrawn",
        "drug stopped",
        "dose reduced",
        "discontinued"
    ],
    "RECHALLENGE": [
        "drug restarted",
        "re-administered",
        "drug readministered"
    ],

    # ── Seriousness Criteria ──────────────────────────────────────────────────
    "HOSPITALISATION": [
        "hospitalised",
        "hospitalized",
        "admitted to hospital",
        "inpatient",
        "hospital admission",
        "icu admission"
    ],
    "LIFE_THREATENING": [
        "life threatening",
        "life-threatening",
        "near fatal",
        "near-fatal",
        "critically ill"
    ],
    "FATAL": [
        "death",
        "died",
        "deceased",
        "fatal outcome",
        "mortality"
    ],

    # ── Outcome Terms ─────────────────────────────────────────────────────────
    "RECOVERED": [
        "resolved",
        "recovery",
        "resolution",
        "returned to baseline",
        "normalised",
        "normalized"
    ],
    "NOT_RECOVERED": [
        "not resolved",
        "ongoing",
        "persisting",
        "persistent",
        "continuing",
        "unresolved"
    ],
    "SEQUELAE": [
        "with sequelae",
        "residual effect",
        "permanent damage",
        "lasting effect"
    ],

    # ── Document & Process Types ──────────────────────────────────────────────
    "SOP": [
        "standard operating procedure",
        "standard procedure",
        "work instruction",
        "wi"
    ],
    "SDEA": [
        "safety data exchange agreement",
        "pharmacovigilance agreement",
        "pv agreement",
        "safety exchange agreement"
    ],
    "PSMF": [
        "pharmacovigilance system master file",
        "pv system master file",
        "master file"
    ],
    "QPPV": [
        "qualified person for pharmacovigilance",
        "qualified pv person",
        "eu qppv"
    ],

    # ── Route of Administration ───────────────────────────────────────────────
    "ORAL": ["po", "by mouth", "per os", "orally", "oral route"],
    "INTRAVENOUS": ["iv", "i.v.", "intravenous infusion", "iv injection", "iv drip"],
    "SUBCUTANEOUS": ["sc", "s.c.", "subcut", "subcutaneously"],
    "INTRAMUSCULAR": ["im", "i.m.", "intramuscularly", "im injection"],
    "TOPICAL": ["applied topically", "topical application", "on skin"],
    "INHALED": ["inhalation", "inhaled route", "via inhaler", "nebulised"],

    # ── Inspection & Audit Terms ──────────────────────────────────────────────
    "CAPA": [
        "corrective and preventive action",
        "corrective action",
        "preventive action",
        "corrective preventive"
    ],
    "AUDIT": [
        "audit finding",
        "audit observation",
        "inspection finding",
        "regulatory inspection",
        "gvp inspection"
    ],
}
