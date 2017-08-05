import requests

try:
    requests.get('https://hub.docker.com', timeout=1)
except Exception:
    print("超时")
