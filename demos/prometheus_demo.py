from flask import Flask
from prometheus_client import start_http_server, Counter, Histogram
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter('app_request_count', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds')


@app.route('/')
def index():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0, 0.2))
    return 'Hello, Prometheus! Visit /metrics on port 8000.'


if __name__ == '__main__':
    # Expose Prometheus metrics on port 8000
    start_http_server(8000)
    # Run demo Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)
