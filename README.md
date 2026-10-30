# Observability & Evidence-Based Incident Diagnosis Platform

A containerized observability platform that monitors application health, detects operational issues, and generates evidence-based incident diagnoses using live Prometheus metrics.

## Overview

This project combines application instrumentation, metrics collection, alerting, visualization, and automated incident diagnosis.

When an alert fires, the diagnosis engine evaluates the alert and supporting metrics to identify a likely cause and recommend remediation steps.

The diagnosis engine uses deterministic, rule-based logic rather than an external LLM.

## Architecture

1. **Flask Application** exposes application endpoints and Prometheus metrics.
2. **Prometheus** scrapes application metrics and evaluates alert rules.
3. **Grafana** visualizes application performance and health.
4. **Evidence Collector** retrieves live metrics from Prometheus.
5. **Diagnosis Engine** evaluates firing alerts against collected evidence.
6. **Diagnosis API** returns the likely root cause, supporting evidence, confidence level, and remediation recommendations.

## Technology Stack

- Python and Flask
- Prometheus
- Grafana
- Docker and Docker Compose
- Python Requests
- Python unittest

## Key Features

- Application instrumentation using Prometheus metrics.
- Request rate, HTTP error rate, and latency monitoring.
- Prometheus alert rules for application failures and performance degradation.
- Grafana dashboard for application observability.
- Evidence collection using live Prometheus queries.
- Rule-based incident diagnosis with root cause, evidence, confidence, and remediation recommendations.
- Configurable failure and latency simulation.

## Monitoring Metrics

| Metric | Description |
|---|---|
| `app_http_requests_total` | Total HTTP requests |
| `app_http_request_duration_seconds` | HTTP request duration |
| `app_http_requests_in_progress` | Requests currently being processed |

## Alert Rules

| Alert | Condition |
|---|---|
| `ApplicationDown` | Application metrics endpoint is unavailable |
| `HighErrorRate` | HTTP 5xx error rate exceeds 10% |
| `HighLatency` | p95 request latency exceeds 1 second |

## Incident Diagnosis

The diagnosis API retrieves firing alerts and collects supporting metrics:

- HTTP 5xx error rate
- p95 request latency
- Application availability

The diagnosis engine evaluates this evidence and returns:

- Alert name and severity
- Likely root cause
- Supporting evidence
- Confidence level
- Recommended remediation actions

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Application homepage |
| `/health` | Application health check |
| `/work` | Simulated application workload |
| `/metrics` | Prometheus metrics endpoint |
| `/diagnose/health` | Diagnosis engine health check |
| `/diagnose` | Evidence-based incident diagnosis |

## Getting Started

### Prerequisites

- Docker Desktop
- Docker Compose

### Run the Platform

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/observability-ai-diagnosis.git
cd observability-ai-diagnosis
```

Build and start the services:

```bash
docker compose up -d --build
```

Verify the containers:

```bash
docker compose ps
```

### Access the Services

| Service | URL |
|---|---|
| Flask Application | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Grafana Dashboard | http://localhost:3000/d/observability-overview/observability-overview |

### Run Unit Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Failure Simulation

The application supports configurable failure and latency simulation through environment variables:

- `ERROR_MODE` — enables or disables simulated HTTP 500 errors.
- `LATENCY_MODE` — enables or disables simulated request latency.

These modes allow monitoring alerts and diagnosis behaviour to be tested under controlled conditions. Disable simulation modes for normal operation.

## Project Structure

```text
observability-ai-diagnosis/
├── app/
│   └── app.py
├── diagnosis/
│   ├── engine.py
│   ├── evidence.py
│   └── prometheus_client.py
├── prometheus/
│   ├── prometheus.yml
│   └── rules/
│       └── application-alerts.yml
├── grafana/
│   ├── dashboards/
│   └── provisioning/
├── tests/
│   └── test_diagnosis_engine.py
├── evidence/
│   └── unit-test-results.txt
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Testing Status

The diagnosis engine includes unit tests covering:

- High error rate diagnosis
- High latency diagnosis
- Application availability diagnosis
- Missing metric evidence
- Unknown alert handling

## Future Improvements

- Expand diagnosis coverage for additional alert types.
- Integrate log analysis into incident diagnosis.
- Add historical incident context.
- Introduce an LLM-based analysis layer with evidence-grounded recommendations.
- Add CI/CD automation for testing and deployment.

---

**Note:** This project demonstrates application observability, metrics-driven alerting, and deterministic incident diagnosis in a containerized environment.
