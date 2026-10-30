from diagnosis.prometheus_client import PrometheusClient


class EvidenceCollector:
    def __init__(self, prometheus=None):
        self.prometheus = prometheus or PrometheusClient()

    def _get_value(self, query):
        result = self.prometheus.query(query)

        if not result:
            return None

        return float(result[0]["value"][1])

    def collect(self):
        error_rate = self._get_value(
            '''
            (
                sum(rate(app_http_requests_total{
                    job="observability-app",
                    status=~"5.."
                }[1m]))
                or vector(0)
            )
            /
            clamp_min(
                sum(rate(app_http_requests_total{
                    job="observability-app"
                }[1m])),
                0.001
            )
            '''
        )

        p95_latency = self._get_value(
            '''
            histogram_quantile(
                0.95,
                sum by (le) (
                    rate(app_http_request_duration_seconds_bucket{
                        job="observability-app"
                    }[1m])
                )
            )
            '''
        )

        availability = self._get_value(
            'up{job="observability-app"}'
        )

        return {
            "error_rate": error_rate,
            "p95_latency_seconds": p95_latency,
            "availability": availability
        }
