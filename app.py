from flask import Flask
from prometheus_client import Counter, Histogram, REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
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
    return 'Hello — Prometheus metrics exposed at /metrics'


def create_app():
    # Mount the Prometheus WSGI app at /metrics so metrics are served from same port
    application = DispatcherMiddleware(app, {
        '/metrics': make_wsgi_app(REGISTRY)
    })
    return application


if __name__ == '__main__':
    # For local development use Flask's built-in server.
    # When using a WSGI server like gunicorn, pass `create_app()` instead of `app`.
    app.run(host='0.0.0.0', port=5000, debug=True)
