import unittest

from backend.classifier import classify_incident
from backend.data_loader import load_incidents
from backend.severity import estimate_severity
from backend.similarity import find_similar_incidents
from fastapi.testclient import TestClient
from backend.app import app


class IncidentPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_analytics_endpoint_counts(self):
        response = self.client.get("/api/analytics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_incidents"], 6)
        self.assertEqual(data["category_counts"]["safety"], 3)
        self.assertEqual(data["category_counts"]["environment"], 2)
        self.assertEqual(data["category_counts"]["esg_compliance"], 1)
        self.assertEqual(data["severity_counts"]["high"], 2)
        self.assertIn("timestamps", data["trend_note"])
        self.assertEqual(data["recurring_patterns"]["PPE non-compliance"], 1)
        self.assertEqual(data["recurring_patterns"]["Oil and chemical spills"], 1)

    def test_analysis_endpoint_response_shape(self):
        response = self.client.post(
            "/api/run",
            json={"text": "Oil seepage observed near wind gearbox maintenance bay"},
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()["result"]
        self.assertEqual(result["category"], "environment")
        self.assertEqual(result["severity"], "high")
        self.assertIn("similar_incidents", result)

    def test_dataset_loads_and_has_required_records(self):
        incidents = load_incidents()
        self.assertEqual(len(incidents), 6)
        self.assertTrue(
            {"incident_id", "narrative", "target_category", "target_severity"}
            .issubset(incidents.columns)
        )

    def test_sample_category_and_severity_labels(self):
        incidents = load_incidents()
        for row in incidents.itertuples(index=False):
            with self.subTest(incident_id=row.incident_id):
                self.assertEqual(
                    classify_incident(row.narrative),
                    row.target_category,
                )
                self.assertEqual(
                    estimate_severity(row.narrative),
                    row.target_severity,
                )

    def test_similarity_returns_matching_incident_first(self):
        results = find_similar_incidents(
            "Contractor slipped near wet walkway and suffered minor injury",
            top_k=3,
        )
        self.assertTrue(results)
        self.assertEqual(results[0]["incident_id"], "S001")
        self.assertGreater(results[0]["similarity_score"], 0)

    def test_unknown_category_for_unmatched_text(self):
        self.assertEqual(
            classify_incident(
                "Routine administrative update with no incident details"
            ),
            "unknown",
        )


if __name__ == "__main__":
    unittest.main()
