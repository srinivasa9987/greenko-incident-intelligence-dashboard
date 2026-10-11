from backend.text_processing import preprocess_text

PREVENTIVE_ACTIONS = {
    "safety": [
        "Inspect the incident area and remove identified safety hazards.",
        "Reinforce safety procedures and provide toolbox training.",
        "Verify the correct use of personal protective equipment (PPE).",
        "Conduct regular workplace safety inspections.",
    ],
    "environment": [
        "Identify and control the source of the leak or spill.",
        "Inspect affected areas and assess potential environmental impact.",
        "Verify that spill containment and response equipment are available.",
        "Conduct preventive maintenance and monitor for recurring leaks.",
    ],
    "esg_compliance": [
        "Review the applicable ESG policy and compliance requirements.",
        "Investigate the cause of the identified deviation.",
        "Retrain responsible personnel on the required procedures.",
        "Introduce periodic compliance inspections and monitoring.",
    ],
    "unknown": [
        "Refer the incident to the responsible safety or ESG team.",
        "Collect additional information before determining corrective actions.",
    ],
}

def suggest_preventive_actions(text, category, severity):
    cleaned_text = preprocess_text(text)
    actions = PREVENTIVE_ACTIONS.get(category,PREVENTIVE_ACTIONS["unknown"]).copy()
    # Add extra actions for high-severity incidents.
    if severity == "high":
        actions.insert(0,"Escalate the incident for immediate assessment by the responsible team.")
    # Add an additional recommendation for spill-related incidents.
    if any(keyword in cleaned_text for keyword in ["oil spill", "chemical spill", "oil seepage"]):
        actions.insert(0,"Contain the spill safely and assess the need for environmental remediation.")
    # Return up to five recommendations without duplicates.
    unique_actions = list(dict.fromkeys(actions))
    return unique_actions[:5]