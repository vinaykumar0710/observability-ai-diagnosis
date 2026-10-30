import logging
import os
import random
import time

from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from diagnosis.prometheus_client import PrometheusClient
from diagnosis.evidence import EvidenceCollector
from diagnosis.engine import DiagnosisEngine

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("observability-app")

REQUESTS = Counter(
    "app_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"],
)

IN_PROGRESS = Gauge(
    "app_http_requests_in_progress",
    "Requests currently being processed",
)

ERROR_MODE = os.getenv("ERROR_MODE", "off")
LATENCY_MODE = os.getenv("LATENCY_MODE", "off")

prometheus_client = PrometheusClient(
    base_url=os.getenv(
        "PROMETHEUS_URL",
        "http://localhost:9090"
    )
)

evidence_collector = EvidenceCollector(prometheus_client)
diagnosis_engine = DiagnosisEngine()


@app.before_request
def start_request():
    request.start_time = time.perf_counter()
    IN_PROGRESS.inc()


@app.after_request
def record_request(response):
    elapsed = time.perf_counter() - getattr(
        request, "start_time", time.perf_counter()
    )

    endpoint = request.url_rule.rule if request.url_rule else "unmatched"

    REQUESTS.labels(
        request.method, endpoint, str(response.status_code)
    ).inc()

    LATENCY.labels(endpoint).observe(elapsed)
    IN_PROGRESS.dec()

    logger.info(
        "method=%s endpoint=%s status=%s duration_seconds=%.4f",
        request.method,
        endpoint,
        response.status_code,
        elapsed,
    )
    return response


@app.route("/")
def home():
    return jsonify(
        service="observability-demo",
        version="1.0.0",
        status="running",
    )


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/work")
def work():
    if ERROR_MODE == "on" and random.random() < 0.5:
        logger.error("Simulated application failure on /work")
        return jsonify(error="simulated_failure"), 500

    if LATENCY_MODE == "on":
        time.sleep(2)

    return jsonify(result="success")


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


@app.route("/diagnose/health")
def diagnosis_health():
    return jsonify(
        service="diagnosis-engine",
        status="available"
    ), 200


@app.route("/diagnose")
def diagnose():
    try:
        alerts = prometheus_client.get_active_alerts()
        evidence = evidence_collector.collect()

        reports = [
            diagnosis_engine.diagnose(alert, evidence)
            for alert in alerts
        ]

        return jsonify(
            status="success",
            active_alert_count=len(alerts),
            evidence=evidence,
            diagnoses=reports
        ), 200

    except Exception:
        logger.exception("Diagnosis request failed")

        return jsonify(
            status="error",
            message="Unable to generate diagnosis. Check application logs."
        ), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
