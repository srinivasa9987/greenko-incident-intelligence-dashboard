from backend.text_processing import preprocess_text
SEVERITY_KEYWORDS = {
    "high": [
        "serious injury",
        "major injury",
        "fatality",
        "fire",
        "explosion",
        "oil spill",
        "oil seepage",
        "chemical spill",
        "near miss",
        "high risk",
        "significant leakage",
    ],
    "medium": [
        "minor injury",
        "slipped",
        "slip",
        "ppe non-compliance",
        "valve leakage",
        "water leakage",
        "housekeeping issue",
        "corrective action",
    ],
    "low": [
        "waste segregation",
        "minor deviation",
        "documentation issue",
        "minor housekeeping issue",
    ],
}

def estimate_severity(text):
    cleaned_text = preprocess_text(text)
    scores = {}
    for severity, keywords in SEVERITY_KEYWORDS.items():
        matched_keywords = [keyword for keyword in keywords if keyword in cleaned_text]
        scores[severity] = len(matched_keywords)
    highest_score = max(scores.values())
    if highest_score == 0:
        return "medium"
    for severity in ["high", "medium", "low"]:
        if scores[severity] == highest_score:
            return severity

def requires_human_review(text, severity):
    cleaned_text = preprocess_text(text)
    review_keywords = [
        "fatality",
        "serious injury",
        "major injury",
        "fire",
        "explosion",
        "near miss",
        "chemical spill",
        "oil spill",
        "unknown",
        "uncertain",
    ]

    if severity == "high":
        return True
    return any(keyword in cleaned_text for keyword in review_keywords)