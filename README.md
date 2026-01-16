# Prometheus-enabled Flask project

This repository contains a minimal Flask application instrumented with Prometheus metrics.

Quick start (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Endpoints
- App: http://localhost:5000/
- Metrics: http://localhost:5000/metrics

Prometheus
- Use `prometheus.yml` as an example scrape config. If Prometheus runs on the same machine, set target to `localhost:5000`.

Notes
- For production, run under a WSGI server (gunicorn/uvicorn) and supply `create_app()` as the WSGI application so `/metrics` remains mounted.
# Prometheus Python demo

This project includes a small demo showing how to expose Prometheus metrics from a Python Flask app.

Prerequisites
- Python 3.8+
- Git (optional)

Install and run (Windows)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python prometheus_demo.py
```

What this runs
- Flask app on http://localhost:5000/ (increments a request counter)
- Prometheus metrics exposed on http://localhost:8000/metrics

Example Prometheus `prometheus.yml` scrape config (add to your Prometheus server config):

```yaml
scrape_configs:
  - job_name: 'python-demo'
    static_configs:
      - targets: ['localhost:8000']
```

Running Prometheus (Windows)
1. Download Prometheus for Windows from https://prometheus.io/download/
2. Place `prometheus.exe` and `prometheus.yml` in the same folder
3. Run:

```powershell
.
\prometheus.exe --config.file=prometheus.yml
```

Visit http://localhost:9090 to open Prometheus web UI and query metrics like `app_request_count`.

Notes
- This demo uses `prometheus_client.start_http_server` to expose metrics on a separate port (8000). In production you can integrate metrics into the same HTTP server or export via WSGI middleware.
