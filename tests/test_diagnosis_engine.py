import unittest

from diagnosis.engine import DiagnosisEngine


class TestDiagnosisEngine(unittest.TestCase):

    def setUp(self):
        self.engine = DiagnosisEngine()

    def test_high_error_rate(self):
        alert = {
            "labels": {
                "alertname": "HighErrorRate",
                "severity": "warning"
            }
        }

        evidence = {
            "error_rate": 0.50,
            "p95_latency_seconds": 0.1,
            "availability": 1.0
        }

        result = self.engine.diagnose(alert, evidence)

        self.assertEqual(result["confidence"], "High")
        self.assertIn("elevated rate", result["root_cause"])

    def test_high_latency(self):
        alert = {
            "labels": {
                "alertname": "HighLatency",
                "severity": "warning"
            }
        }

        evidence = {
            "error_rate": 0.0,
            "p95_latency_seconds": 2.0,
            "availability": 1.0
        }

        result = self.engine.diagnose(alert, evidence)

        self.assertEqual(result["confidence"], "High")
        self.assertIn("latency is elevated", result["root_cause"])

    def test_application_down(self):
        alert = {
            "labels": {
                "alertname": "ApplicationDown",
                "severity": "critical"
            }
        }

        evidence = {
            "error_rate": 0.0,
            "p95_latency_seconds": 0.1,
            "availability": 0.0
        }

        result = self.engine.diagnose(alert, evidence)

        self.assertEqual(result["confidence"], "High")
        self.assertIn("cannot scrape", result["root_cause"])

    def test_unknown_alert(self):
        alert = {
            "labels": {
                "alertname": "UnknownAlert",
                "severity": "warning"
            }
        }

        evidence = {}

        result = self.engine.diagnose(alert, evidence)

        self.assertEqual(result["confidence"], "Low")
        self.assertIn("No diagnostic rule", result["evidence"][0])

    def test_missing_error_rate_evidence(self):
        alert = {
            "labels": {
                "alertname": "HighErrorRate",
                "severity": "warning"
            }
        }

        result = self.engine.diagnose(alert, {})

        self.assertEqual(result["confidence"], "Low")
        self.assertIn("unavailable", result["evidence"][0])


if __name__ == "__main__":
    unittest.main()