import os
import time
import random
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY = os.environ.get('PUSHGATEWAY', '172.18.24.206:9091')

registry = CollectorRegistry()
g = Gauge('batch_random_value', 'Random value produced by batch job', registry=registry)

def push_once():
    v = random.random() * 100
    g.set(v)
    push_to_gateway(PUSHGATEWAY, job='batch_job', registry=registry)
    print(f'pushed {v} to {PUSHGATEWAY}')

if __name__ == '__main__':
    interval = int(os.environ.get('PUSH_INTERVAL', '5'))
    while True:
        try:
            push_once()
        except Exception as e:
            print('push failed:', e)
        time.sleep(interval)
