# Architecture — myPythonProject

This document describes the architecture of the Prometheus-enabled Flask demo repository.

Components
- `app` — Flask application instrumented with `prometheus_client`. Exposes application metrics at `/metrics`.
- `wsgi` — `gunicorn` WSGI entrypoint for production deployments; `wsgi.py` exposes `create_app()` which mounts `/metrics` via `DispatcherMiddleware`.
- `prometheus` — collects metrics from `app`, `pushgateway`, `blackbox-exporter`, and other exporters.
- `pushgateway` — receives pushes from the `pusher` batch job (`push_metrics.py`). Prometheus scrapes Pushgateway to collect pushed metrics.
- `pusher` — simple continuous job that pushes a `batch_random_value` Gauge to Pushgateway every few seconds.
- `blackbox-exporter` — probes external websites (HTTP/HTTPS) and exposes probe metrics (success, latency, status).
- `grafana` — visualization layer; queries Prometheus and renders dashboards.

Data flows
1. User/Developer traffic hits `app` (Flask). `app` increments counters and records latencies.
2. Prometheus scrapes `app` `/metrics` endpoint at intervals and stores time series.
3. `pusher` periodically runs `push_metrics.py` and pushes `batch_random_value` to `pushgateway`.
4. Prometheus scrapes `pushgateway` and ingests pushed metrics.
5. `blackbox-exporter` probes configured external sites (e.g., example.com). Prometheus scrapes the exporter at `/probe` to collect probe metrics.
6. Grafana queries Prometheus for dashboards (app request rate, pushed values, probe success/latency).

Deployment
- All components are provided in `docker-compose.yml` for local testing: `app`, `prometheus`, `pushgateway`, `pusher`, `blackbox-exporter`, `grafana`.
- `prometheus.yml` contains scrape configs for `app`, `pushgateway`, and `blackbox` probes.

Useful PromQL queries
- Current pushed value: `batch_random_value`
- App request rate: `rate(app_request_count[1m])`
- App request latency (histogram): `histogram_quantile(0.95, sum(rate(app_request_latency_seconds_bucket[5m])) by (le))`
- Probe success: `probe_success{job="blackbox-probes"}`
- Probe latency: `probe_duration_seconds{job="blackbox-probes"}`

See `docs/architecture.puml` for a PlantUML diagram you can render with any PlantUML tool.
