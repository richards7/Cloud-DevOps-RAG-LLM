import urllib.request
import urllib.error
import json

req = urllib.request.Request(
    'http://127.0.0.1:8080/chat',
    data=b'{"query": "What is the difference between a Docker image and a container?"}',
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as res:
        print("Success:", res.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}:", e.read().decode())
except Exception as e:
    print("Error:", e)
