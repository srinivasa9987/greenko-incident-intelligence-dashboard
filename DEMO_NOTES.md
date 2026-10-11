# Demo Notes

1. Start the application with `python -m uvicorn backend.app:app --reload`.
2. Open `/` to see historical analytics and the incident analysis form.
3. The sample analytics should report 6 total incidents: 3 safety, 2 environment, 1 ESG compliance; severity counts are 1 low, 3 medium, and 2 high.
4. Submit the sample oil-seepage narrative to `/api/run` or through the form. Expected sample behavior: category `environment`, severity `high`, related historical incident S002, preventive recommendations, and a human-review flag.
5. `/docs` provides interactive FastAPI API documentation.

The bundled dataset is synthetic and has no timestamps. Analytics are sample record distributions and keyword-based recurring-pattern counts, not company-wide rates or time-based trends. The six-row label check is a regression smoke test, not a statistically meaningful accuracy result.
