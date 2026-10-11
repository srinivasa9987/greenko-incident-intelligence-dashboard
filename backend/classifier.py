from backend.text_processing import preprocess_text

CATEGORY_KEYWORDS = {
    "safety": [
        "injury",
        "injured",
        "slipped",
        "slip",
        "fell",
        "fall",
        "near miss",
        "ppe non-compliance",
        "ppe",
        "personal protective equipment",
        "unsafe condition",
        "vehicle movement",
        "cable trench",
        "housekeeping",
        "contractor safety",
    ],
    "environment": [
        "oil seepage",
        "oil spill",
        "oil leakage",
        "spill",
        "water usage",
        "water consumption",
        "water leakage",
        "valve leakage",
        "wastewater",
        "water pollution",
        "environmental",
        "gearbox",
    ],
    "esg_compliance": [
        "waste segregation",
        "segregation deviation",
        "compliance",
        "non-compliance",
        "deviation",
        "policy violation",
        "regulatory",
    ],
}


def classify_incident(text):
    cleaned_text = preprocess_text(text)
    scores = {
        category: sum(
            1 for keyword in keywords if keyword in cleaned_text
        )
        for category, keywords in CATEGORY_KEYWORDS.items()
    }

    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "unknown"
    return best_category


def explain_classification(text, category):
    cleaned_text = preprocess_text(text)
    keywords = CATEGORY_KEYWORDS.get(category, [])
    matched_keywords = [
        keyword for keyword in keywords if keyword in cleaned_text
    ]

    if matched_keywords:
        explanation = (
            f"Category '{category}' matched these keywords: "
            f"{', '.join(matched_keywords)}."
        )
    else:
        explanation = (
            "No category-specific keywords matched. "
            "Manual review is recommended."
        )

    return {
        "category": category,
        "matched_keywords": matched_keywords,
        "explanation": explanation,
    }
