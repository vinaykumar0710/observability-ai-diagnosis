import os
import requests


class PrometheusClient:
    def __init__(self, base_url=None, timeout=5):
        self.base_url = (
            base_url or os.getenv(
                "PROMETHEUS_URL",
                "http://localhost:9090"
            )
        ).rstrip("/")
        self.timeout = timeout

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()

        payload = response.json()

        if payload.get("status") != "success":
            raise RuntimeError(
                f"Prometheus API error: {payload}"
            )

        return payload["data"]

    def get_active_alerts(self):
        data = self._get("/api/v1/alerts")

        return [
            alert
            for alert in data.get("alerts", [])
            if alert.get("state") == "firing"
        ]

    def query(self, expression):
        data = self._get(
            "/api/v1/query",
            params={"query": expression}
        )

        return data.get("result", [])
