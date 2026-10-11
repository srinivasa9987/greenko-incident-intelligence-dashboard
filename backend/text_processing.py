import re


def validate_incident_input(text):
    if not isinstance(text, str):
        raise TypeError("Incident description must be a string.")
    text = text.strip()
    if not text:
        raise ValueError("Incident description cannot be empty.")
    if len(text) < 10:
        raise ValueError("Incident description must contain at least 10 characters.")
    if len(text) > 2000:
        raise ValueError("Incident description cannot exceed 2000 characters.")
    return True

def preprocess_text(text):
    validate_incident_input(text)
    cleaned_text = text.lower()
    # Replace tabs, newlines, and repeated whitespace
    # with a single space.
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()