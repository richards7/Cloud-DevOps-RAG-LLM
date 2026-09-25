# Python (for DevOps/Cloud automation)

## Why Python for DevOps
Python is the most common automation/scripting language in cloud and DevOps work —
used for CI/CD scripts, cloud SDKs (boto3 for AWS, google-cloud-* for GCP), automation
tooling (Ansible is Python-based), and glue code between systems.

## File and system operations
```python
import os
import shutil
import subprocess

os.listdir(".")                       # list files in current dir
os.path.exists("file.txt")              # check if a path exists
os.makedirs("a/b/c", exist_ok=True)       # create nested dirs, no error if exists
shutil.copy("a.txt", "b.txt")               # copy a file
shutil.rmtree("old_dir")                      # delete a directory recursively

result = subprocess.run(
    ["ls", "-la"], capture_output=True, text=True
)
print(result.stdout)
```

## Working with environment variables and .env files
```python
import os
from dotenv import load_dotenv

load_dotenv()  # reads a .env file into the environment
api_key = os.getenv("API_KEY", "default_value")
```

## Making HTTP requests (calling REST APIs)
```python
import requests

response = requests.get("https://api.example.com/data")
response.raise_for_status()   # raises an exception on 4xx/5xx
data = response.json()

response = requests.post(
    "https://api.example.com/items",
    json={"name": "test"},
    headers={"Authorization": f"Bearer {token}"},
)
```

## Cloud SDK basics (AWS example — boto3)
```python
import boto3

s3 = boto3.client("s3")
s3.upload_file("local.txt", "my-bucket", "remote.txt")

response = s3.list_objects_v2(Bucket="my-bucket")
for obj in response.get("Contents", []):
    print(obj["Key"])
```

## Error handling patterns
```python
try:
    risky_operation()
except FileNotFoundError as e:
    print(f"File missing: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    cleanup()
```

## Logging (preferred over print() for real scripts)
```python
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

logger.info("Starting deployment")
logger.warning("Config value missing, using default")
logger.error("Deployment failed: %s", str(error))
```

## A simple automation script pattern
```python
#!/usr/bin/env python3
"""Check a list of URLs and alert if any are down."""
import sys
import requests

URLS = ["https://example.com", "https://api.example.com/health"]

def check(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False

def main():
    failures = [u for u in URLS if not check(u)]
    if failures:
        print(f"DOWN: {failures}")
        sys.exit(1)
    print("All services healthy.")

if __name__ == "__main__":
    main()
```

## Common errors & fixes
- **`ModuleNotFoundError`**: package isn't installed in the active environment —
  confirm you're in the right virtualenv (`which python`) and run
  `pip install -r requirements.txt`.
- **`FileNotFoundError` for a relative path**: the script's working directory isn't
  what you assumed — use `os.path.dirname(os.path.abspath(__file__))` to build paths
  relative to the script itself, not the caller's current directory.
- **Environment variable is `None`**: `.env` wasn't loaded, or the variable name has a
  typo — print `os.environ` to debug, and confirm `load_dotenv()` runs before the
  variable is read.
- **`requests.exceptions.SSLError`**: often a corporate proxy/firewall intercepting
  TLS — verify the actual cause before disabling verification (`verify=False` is a
  security risk, not a real fix).
