from backend.text_processing import preprocess_text

def generate_summary(text):
    cleaned_text = preprocess_text(text)
    # Return short descriptions without unnecessary processing.
    if len(cleaned_text) <= 160:
        return cleaned_text.capitalize()
    sentences = [sentence.strip() for sentence in cleaned_text.split(".") if sentence.strip()]
    if not sentences:
        return cleaned_text[:160].capitalize()
    summary = ". ".join(sentences[:2])
    # Limit the summary length.
    if len(summary) > 160:
        summary = summary[:157].rstrip() + "..."
    return summary[0].upper() + summary[1:]