# Greenko ESG / Safety Incident Intelligence Dashboard

## Overview
A small FastAPI + HTML/CSS/JavaScript application that analyzes safety, environmental, and ESG-compliance incident narratives for review. It is built to run with the bundled dummy dataset and does not require external API keys.

## Features
- Rule-based incident category classification with matched-keyword explanations.
- Heuristic severity estimate and human-review flag.
- Short text summary.
- TF-IDF/cosine-similarity retrieval of related historical incidents.
- Category-aware preventive actions, including escalation guidance for high-severity estimates.
- Historical analytics endpoint and dashboard: total incidents, category distribution, severity distribution, and keyword-based recurring patterns.
- API validation and a small regression test suite.

## Technology choices and assumptions
- **FastAPI** serves the API and the single-page frontend.
- **Pandas** loads and validates the CSV.
- **scikit-learn TF-IDF + cosine similarity** provides a lightweight local retrieval baseline; this is retrieval, not a full embedding-based RAG/LLM system.
- Classification and severity tagging are transparent keyword heuristics, not trained predictive models.
- Summaries are short text transformations, not generative AI summaries.
- Analytics count records in the bundled sample. The CSV has no timestamp field, so the app does not claim monthly/weekly trends. Recurring patterns are simple keyword counts and may overlap.
- The included dataset contains only six synthetic examples. Agreement with these six labels is a smoke/regression check, not a reliable estimate of real-world model accuracy.

## Project structure
```text
backend/       FastAPI routes and incident processing modules
data/          Bundled sample incident CSV
frontend/      HTML/CSS/JavaScript dashboard
tests/         Regression tests
Procfile       Railway web process command
requirements.txt
```

## Run locally
Use Python 3.10+ (Python 3.11 is a sensible deployment target).

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn backend.app:app --reload
```

Open:
- Dashboard: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs
- Demo status: http://127.0.0.1:8000/api/demo
- Historical analytics: http://127.0.0.1:8000/api/analytics
- Historical incidents: http://127.0.0.1:8000/api/incidents

## Run tests
From the project root:
```bash
python -m unittest discover -s tests -v
```

## Main API
- `GET /api/demo` — app status and expected outcome.
- `GET /api/analytics` — category/severity counts and recurring keyword patterns.
- `GET /api/incidents` — validated historical records.
- `POST /api/run` — submit `{"text": "..."}` and receive classification, severity, summary, similar incidents, recommendations, and limitations.

## Evaluation and limitations
The regression suite checks the six supplied sample narratives against their bundled labels, checks that an unrelated narrative is classified as `unknown`, and verifies that the closest text match is retrieved first. These checks validate expected starter behavior only; they are not a held-out evaluation set.

Known limitations:
- Very small synthetic dataset; results will not generalize without additional labeled incidents.
- Keyword rules can miss paraphrases and may match multiple concepts.
- Severity depends on narrative wording and must not replace formal risk assessment.
- TF-IDF similarity measures lexical overlap, not shared cause or operational relevance.
- No incident timestamps means temporal trend extraction is not supported.
- Recommendations are general and require qualified review.
- No authentication, role-based access, audit trail, or production monitoring is included.

## Deploy to Railway
The repository includes a `Procfile` that starts the FastAPI app on Railway's assigned `$PORT`.

1. Push the project root (the directory containing `Procfile`, `requirements.txt`, `backend/`, `frontend/`, and `data/`) to a GitHub repository.
2. In Railway, create a project and deploy from that GitHub repository.
3. Confirm the service root is the project root; do not deploy from a parent directory that only contains the nested project folder.
4. Railway should install dependencies from `requirements.txt` and use the `Procfile` web command.
5. After deployment, open the public domain and verify `/`, `/api/demo`, `/api/analytics`, `/api/incidents`, and `/docs`.
6. Add the generated Railway public domain to the submission notes.

A live Railway URL cannot be included until deployment is performed in the user's Railway account. Do not report deployment as completed until the public URL has been tested.
