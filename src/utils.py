from prometheus_client import Counter, Histogram

# Centralized Metrics - Names must match app.py exactly
REQUEST_COUNT = Counter(
    'app_request_count', 
    'Total HTTP requests to the application'
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 
    'Time spent processing requests in seconds'
)