"""Simple load generator that hits the app root to produce Prometheus metrics."""
import os
import time
import urllib.request

URL = os.environ.get('LOAD_URL', 'http://localhost:5000/')
INTERVAL = float(os.environ.get('LOAD_INTERVAL', '1'))

def hit():
    try:
        with urllib.request.urlopen(URL, timeout=5) as r:
            r.read()
        print('hit', URL)
    except Exception as e:
        print('hit failed:', e)

if __name__ == '__main__':
    print('Starting load generator, hitting', URL, 'every', INTERVAL, 's')
    while True:
        hit()
        time.sleep(INTERVAL)
