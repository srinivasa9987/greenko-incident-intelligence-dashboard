from functools import lru_cache
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import re
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.data_loader import load_incidents
from backend.text_processing import validate_incident_input
from backend.classifier import classify_incident,explain_classification
from backend.severity import estimate_severity,requires_human_review
from backend.summarizer import generate_summary
from backend.similarity import find_similar_incidents
from backend.recommendations import suggest_preventive_actions
app = FastAPI(title="ESG / Safety Incident Intelligence Dashboard")
BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
FRONTEND = BASE / "frontend"
app.mount("/frontend",StaticFiles(directory=FRONTEND),name="frontend",)
@app.get("/")
def homepage():
    return FileResponse(FRONTEND / "index.html")
class Query(BaseModel):
    text: str = Field(...,min_length=10,max_length=2000,)
@lru_cache(maxsize=1)
def get_incident_data():
    return load_incidents()
@app.get("/api/demo")
def demo():
    return {
        "case_study": ("ESG / Safety Incident Intelligence Dashboard"),
        "status": "starter app running",
        "expected_outcome": ("A dashboard that classifies incident type, severity, "
            "recurring patterns, and recommended preventive actions "
            "using NLP and summarization logic."),
    }

def analyze_incident(text):
    validate_incident_input(text)
    category = classify_incident(text)
    classification_explanation = explain_classification(text,category,)
    severity = estimate_severity(text)
    summary = generate_summary(text)
    df = get_incident_data()
    similar_incidents = find_similar_incidents(text,top_k=3,)
    preventive_actions = suggest_preventive_actions(text,category,severity,)
    human_review_required = requires_human_review(text,severity)
    return {
        "input": text,
        "summary": summary,
        "category": category,
        "severity": severity,
        "classification_explanation": (
            classification_explanation
        ),
        "similar_incidents": similar_incidents,
        "preventive_actions": preventive_actions,
        "human_review_required": human_review_required,
        "limitations": [
            "Classification uses keyword-based rules.",
            "Severity is an initial estimate, not a formal assessment.",
            "Textual similarity does not establish a shared root cause.",
            "Recommendations require review by qualified personnel.",
        ],
    }


@app.post("/api/run")
def run_case(query: Query):
    try:
        result = analyze_incident(query.text)
        return {
            "input": query.text,
            "result": result,
            "evaluation_hint": (
                "Review predictions, retrieval evidence, "
                "severity estimates, recommendations, and limitations."
            ),
        }
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="Historical incident dataset was not found.",
        ) from exc

    except Exception as exc:
        # Replace with structured logging in production.
        raise HTTPException(
            status_code=500,
            detail="Incident analysis failed.",
        ) from exc


@app.get("/api/analytics")
def get_analytics():
    try:
        df = get_incident_data()

        # Support the original CSV column names and normalized names.
        category_col = (
            "category" if "category" in df.columns
            else "target_category"
        )

        severity_col = (
            "severity" if "severity" in df.columns
            else "target_severity"
        )

        category_counts = (
            df[category_col]
            .fillna("unknown")
            .astype(str)
            .str.lower()
            .value_counts()
            .to_dict()
        )

        severity_counts = (
            df[severity_col]
            .fillna("unknown")
            .astype(str)
            .str.lower()
            .value_counts()
            .to_dict()
        )

        # Identify common patterns in historical descriptions.
        narrative_col = "narrative"

        patterns = {
            "PPE non-compliance": [r"\bppe\b", "protective equipment"],
            "Slips and falls": [r"\bslipped\b", r"\bslip\b", r"\bfall\b"],
            "Oil and chemical spills": [
                "oil seepage", "oil spill", "oil leakage",
                "chemical spill", "spill kit",
            ],
            "Vehicle movement": ["vehicle", "traffic"],
            "Waste management": ["waste segregation", "waste"],
            "Water usage and leakage": ["water usage", "water", "valve leakage"],
        }

        recurring_patterns = {}

        if narrative_col in df.columns:
            narratives = (
                df[narrative_col]
                .fillna("")
                .astype(str)
                .str.lower()
                .tolist()
            )

            for pattern, keywords in patterns.items():
                count = sum(
                    any(
                        bool(re.search(keyword, narrative))
                        if keyword.startswith(r"\b")
                        else keyword in narrative
                        for keyword in keywords
                    )
                    for narrative in narratives
                )
                if count > 0:
                    recurring_patterns[pattern] = count

        return {
            "total_incidents": len(df),
            "category_counts": category_counts,
            "severity_counts": severity_counts,
            "recurring_patterns": recurring_patterns,
            "trend_note": (
                "These are historical distributions and recurring patterns. "
                "Time-based trends require incident timestamps."
            ),
        }

    except (FileNotFoundError, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to calculate historical incident analytics.",
        ) from exc
    
@app.get("/api/incidents")
def get_incidents():
    try:
        df = get_incident_data()

        safe_df = df.astype(object).where(
            pd.notna(df),
            None,
        )

        return {
            "count": len(safe_df),
            "incidents": safe_df.to_dict(
                orient="records"
            ),
        }

    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to load historical incidents.",
        ) from exc