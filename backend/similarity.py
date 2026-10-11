from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.text_processing import preprocess_text
from backend.data_loader import load_incidents

def find_similar_incidents(text, top_k=3):
    cleaned_text = preprocess_text(text)
    incidents = load_incidents()
    if incidents.empty:
        return []
    narratives = incidents["narrative"].fillna("").astype(str).tolist()
    cleaned_narratives = [preprocess_text(narrative) if narrative.strip() else "" for narrative in narratives]
    # Convert descriptions into numerical vectors.
    vectorizer = TfidfVectorizer()
    try:
        historical_vectors = vectorizer.fit_transform(cleaned_narratives)
        new_vector = vectorizer.transform([cleaned_text])
    except ValueError:
        return []
    similarity_scores = cosine_similarity(new_vector,historical_vectors)[0]
    # Sort incidents from highest to lowest similarity.
    ranked_indices = similarity_scores.argsort()[::-1]
    results = []
    for index in ranked_indices:
        score = float(similarity_scores[index])
        # Ignore unrelated incidents.
        if score <= 0:
            continue
        incident = incidents.iloc[index]
        results.append({
            "incident_id": str(incident["incident_id"]),
            "narrative": str(incident["narrative"]),
            "category": str(incident["target_category"]),
            "severity": str(incident["target_severity"]),
            "similarity_score": round(score, 4),
        })
        if len(results) >= top_k:
            break

    return results