import time
import random
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, REGISTRY

# Import your metrics from the src folder
from src.utils import REQUEST_COUNT, REQUEST_LATENCY

app = Flask(__name__)

@app.route('/')
def index():
    # Increment our centralized counter
    REQUEST_COUNT.inc()
    
    # Track latency using the centralized histogram
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0, 0.2))
        
    return 'Hello — Prometheus metrics exposed at /metrics'

def create_app():
    """Factory to create the WSGI application with metrics middleware."""
    # Mount /metrics to the Prometheus WSGI app
    return DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app(REGISTRY)
    })

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    
    # Create the combined application
    application = create_app()
    
    print("🚀 Server starting at http://localhost:5000")
    print("📊 Metrics available at http://localhost:5000/metrics")
    
    # Run the server
    run_simple('0.0.0.0', 5000, application, use_reloader=True)