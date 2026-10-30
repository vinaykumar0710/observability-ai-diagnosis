class DiagnosisEngine:

    def diagnose(self, alert, evidence):
        alert_name = alert.get("labels", {}).get("alertname")
        severity = alert.get("labels", {}).get("severity", "unknown")

        error_rate = evidence.get("error_rate")
        latency = evidence.get("p95_latency_seconds")
        availability = evidence.get("availability")

        result = {
            "alert": alert_name,
            "severity": severity,
            "root_cause": "Insufficient evidence to determine the likely cause.",
            "evidence": [],
            "confidence": "Low",
            "remediation": [
                "Inspect application logs.",
                "Review Prometheus metrics.",
                "Check application and infrastructure health."
            ]
        }

        if alert_name == "HighErrorRate":
            if error_rate is None:
                result["evidence"].append(
                    "HTTP 5xx error-rate metric is unavailable."
                )
            else:
                result["evidence"].append(
                    f"Observed HTTP 5xx error rate: {error_rate:.2%}."
                )

                if error_rate > 0.10:
                    result["root_cause"] = (
                        "Application is experiencing an elevated rate "
                        "of HTTP 5xx responses."
                    )
                    result["confidence"] = "High"
                    result["remediation"] = [
                        "Inspect application logs for exceptions.",
                        "Identify the endpoint generating HTTP 5xx responses.",
                        "Check recent deployments and dependency failures."
                    ]
                else:
                    result["root_cause"] = (
                        "The current HTTP 5xx error rate is below "
                        "the configured alert threshold."
                    )
                    result["confidence"] = "Medium"

        elif alert_name == "HighLatency":
            if latency is None:
                result["evidence"].append(
                    "p95 latency measurement is unavailable."
                )
            else:
                result["evidence"].append(
                    f"Observed p95 latency: {latency:.4f} seconds."
                )

                if latency > 1.0:
                    result["root_cause"] = (
                        "Application response latency is elevated."
                    )
                    result["confidence"] = "High"
                    result["remediation"] = [
                        "Identify slow application endpoints.",
                        "Inspect CPU and memory utilization.",
                        "Investigate database and external service latency."
                    ]
                else:
                    result["root_cause"] = (
                        "Current p95 latency is below the configured "
                        "alert threshold."
                    )
                    result["confidence"] = "Medium"

        elif alert_name == "ApplicationDown":
            if availability is None:
                result["evidence"].append(
                    "Application availability metric is unavailable."
                )
            else:
                result["evidence"].append(
                    f"Observed application availability: {availability}."
                )

                if availability == 0:
                    result["root_cause"] = (
                        "Prometheus cannot scrape the application metrics "
                        "endpoint."
                    )
                    result["confidence"] = "High"
                    result["remediation"] = [
                        "Check application container status.",
                        "Inspect application container logs.",
                        "Verify application health and network connectivity."
                    ]
                else:
                    result["root_cause"] = (
                        "Application availability is currently healthy, "
                        "although the alert may reflect an earlier failure."
                    )
                    result["confidence"] = "Medium"

        else:
            result["evidence"].append(
                "No diagnostic rule exists for this alert."
            )

        return result
