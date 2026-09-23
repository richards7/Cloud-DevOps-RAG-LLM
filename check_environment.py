"""
Environment readiness check for the Cloud & DevOps RAG Assistant project.

Checks:
  - Python version
  - pip and key packages
  - Docker installed / running
  - Whether the ports this project needs (8080, 8000) are already in use,
    and by what, with the command to free them

Run:
    python check_environment.py
"""
import shutil
import socket
import subprocess
import sys
import platform

PORTS_TO_CHECK = [8080, 8000, 5432]  # 8080/8000: API, 5432: in case you add Postgres later

OS_NAME = platform.system()  # "Windows", "Linux", "Darwin" (mac)


def header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def check_python():
    header("Python")
    v = sys.version_info
    print(f"Python version: {v.major}.{v.minor}.{v.micro}")
    if v.major == 3 and v.minor >= 10:
        print("OK — Python 3.10+ detected.")
    else:
        print("WARNING — this project expects Python 3.10 or newer.")


def check_pip():
    header("pip")
    pip_path = shutil.which("pip") or shutil.which("pip3")
    if pip_path:
        print(f"pip found at: {pip_path}")
    else:
        print("WARNING — pip not found on PATH.")


def check_command(name, version_flag="--version"):
    path = shutil.which(name)
    if not path:
        print(f"{name}: NOT FOUND")
        return False
    try:
        result = subprocess.run(
            [name, version_flag], capture_output=True, text=True, timeout=5
        )
        out = (result.stdout or result.stderr).strip().splitlines()[0]
        print(f"{name}: {out}")
        return True
    except Exception as e:
        print(f"{name}: found at {path}, but version check failed ({e})")
        return True


def check_docker():
    header("Docker")
    found = check_command("docker")
    if found:
        try:
            result = subprocess.run(
                ["docker", "info"], capture_output=True, text=True, timeout=8
            )
            if result.returncode == 0:
                print("Docker daemon is running.")
            else:
                print("Docker is installed but the daemon doesn't seem to be "
                      "running. Start Docker Desktop (or `sudo systemctl start "
                      "docker` on Linux) before running docker build/run.")
        except Exception:
            print("Could not confirm whether the Docker daemon is running.")
    else:
        print("Docker not found. Install it from https://docker.com/get-started "
              "if you plan to containerize/deploy tonight; it's optional for "
              "running the API locally with uvicorn.")


def check_git():
    header("Git")
    check_command("git")


def is_port_open(port, host="127.0.0.1"):
    """Returns True if the port is FREE (nothing listening)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((host, port))
        return result != 0  # non-zero = connection failed = port is free


def find_process_on_port(port):
    """Best-effort lookup of what's using a port, OS-specific."""
    try:
        if OS_NAME == "Windows":
            cmd = f'netstat -ano | findstr :{port}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:  # Linux / Mac
            cmd = f"lsof -i :{port}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
    except Exception as e:
        return f"(couldn't check: {e})"


def check_ports():
    header("Ports this project uses")
    for port in PORTS_TO_CHECK:
        free = is_port_open(port)
        if free:
            print(f"Port {port}: FREE — ready to use.")
        else:
            print(f"Port {port}: IN USE")
            details = find_process_on_port(port)
            if details:
                print(f"  Currently used by:\n  {details}")
            print(f"  --> See 'How to free a port' below to stop it, or run "
                  f"this project on a different port instead (see options below).")


def print_free_port_instructions():
    header("How to free a port")
    if OS_NAME == "Windows":
        print("""1. Find the PID using the port:
     netstat -ano | findstr :8080
   (last column in the output is the PID)

2. Kill that process:
     taskkill /PID <pid_number> /F
""")
    else:
        print("""1. Find the PID using the port:
     lsof -i :8080

2. Kill that process:
     kill -9 <pid_number>

   Or in one line:
     kill -9 $(lsof -t -i :8080)
""")
    print("""If you'd rather NOT kill the other process, just run this project
on a different port instead:

  uvicorn app.main:app --reload --port 8081

  # and for Docker:
  docker run -p 8081:8080 --env-file .env cloud-rag-assistant
  (host_port:container_port — only the left number needs to change)
""")


def check_required_packages():
    header("Key Python packages (only meaningful if run inside your venv)")
    packages = ["fastapi", "uvicorn", "chromadb", "google.generativeai", "openai", "sqlalchemy"]
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"{pkg}: installed")
        except ImportError:
            print(f"{pkg}: NOT installed (run: pip install -r requirements.txt)")


def main():
    print("Cloud & DevOps RAG Assistant — Environment Check")
    print(f"OS: {OS_NAME}")

    check_python()
    check_pip()
    check_required_packages()
    check_git()
    check_docker()
    check_ports()
    print_free_port_instructions()

    header("Done")
    print("Fix anything marked WARNING/NOT FOUND above, then proceed with "
          "scripts/ingest.py and uvicorn.")


if __name__ == "__main__":
    main()