from backend.classifier import classify_incident
from backend.severity import estimate_severity
from backend.similarity import find_similar_incidents
from backend.data_loader import load_incidents


print("=" * 60)
print("1. HISTORICAL DATASET")
print("=" * 60)

df = load_incidents()

print("Dataset loaded successfully.")
print("Incident count:", len(df))
print()


print("=" * 60)
print("2. CLASSIFICATION AND SEVERITY")
print("=" * 60)

test_cases = [
    (
        "Contractor slipped near wet walkway, minor injury",
        "safety",
        "medium",
    ),
    (
        "Oil seepage observed near wind gearbox maintenance bay, "
        "contained with spill kit",
        "environment",
        "high",
    ),
    (
        "PPE non-compliance observed during panel cleaning activity",
        "safety",
        "medium",
    ),
    (
        "Near miss: vehicle movement close to cable trench",
        "safety",
        "high",
    ),
    (
        "Water usage spike during module cleaning due to valve leakage",
        "environment",
        "medium",
    ),
    (
        "Repeated waste segregation deviation at contractor storage area",
        "esg_compliance",
        "low",
    ),
]

for text, expected_category, expected_severity in test_cases:
    category = classify_incident(text)
    severity = estimate_severity(text)

    print("Incident:", text)
    print("Expected category:", expected_category)
    print("Predicted category:", category)
    print("Expected severity:", expected_severity)
    print("Predicted severity:", severity)

    print(
        "Category correct:",
        category == expected_category,
    )
    print(
        "Severity correct:",
        severity == expected_severity,
    )
    print("-" * 60)


print("=" * 60)
print("3. SIMILAR INCIDENT RETRIEVAL")
print("=" * 60)

query = (
    "Contractor slipped near wet walkway and suffered minor injury"
)

results = find_similar_incidents(query, top_k=3)

print("Retrieved incidents:", len(results))

for incident in results:
    print(incident)