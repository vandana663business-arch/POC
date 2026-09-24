"""One-shot launcher for the Intake Staffing Forecasting POC.

Run this from the POC project root with any Python 3.10+:

    python run.py

What it does, in order:
1. Ensures a single virtual environment exists at <POC root>/venv (creates it
   if missing) -- this is the ONLY venv for the project; backend and
   frontend folders do not get their own.
2. Ensures every package in requirements.txt (project root) is installed
   into that venv (installs whatever is missing).
3. Ensures frontend/node_modules exists (runs `npm install` if missing).
4. Starts the FastAPI backend (http://127.0.0.1:8000).
5. Starts the React/Vite frontend (http://localhost:5173) and opens it in
   your browser.

Press Ctrl+C to stop both servers.
"""

import os
import subprocess
import sys
import time
import venv as venv_module
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / "venv"
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
REQUIREMENTS_FILE = ROOT / "requirements.txt"

IS_WINDOWS = os.name == "nt"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")
NPM_CMD = "npm.cmd" if IS_WINDOWS else "npm"


def ensure_single_venv():
    stray = [
        p
        for p in (BACKEND_DIR / "venv", FRONTEND_DIR / "venv")
        if p.exists()
    ]
    for p in stray:
        print(f"[venv] Removing stray virtual environment at {p} (only {VENV_DIR} should exist)...")
        import shutil

        shutil.rmtree(p)

    if VENV_PYTHON.exists():
        print(f"[venv] Using existing virtual environment at {VENV_DIR}")
        return
    print(f"[venv] No virtual environment found at {VENV_DIR}, creating one...")
    venv_module.create(VENV_DIR, with_pip=True)
    print("[venv] Created.")


def installed_packages() -> set:
    result = subprocess.run(
        [str(VENV_PYTHON), "-m", "pip", "list", "--format=freeze"],
        capture_output=True,
        text=True,
        check=True,
    )
    names = set()
    for line in result.stdout.splitlines():
        if "==" in line:
            names.add(line.split("==")[0].lower())
    return names


def required_packages() -> list:
    names = []
    for line in REQUIREMENTS_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        base = line.split("[")[0].split("==")[0].split(">=")[0].strip()
        names.append(base.lower())
    return names


def ensure_backend_dependencies():
    installed = installed_packages()
    required = required_packages()
    missing = [r for r in required if r not in installed]
    if missing:
        print(f"[deps] Missing packages: {', '.join(missing)}. Installing from requirements.txt...")
        subprocess.run(
            [str(VENV_PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            check=True,
        )
        print("[deps] Installed.")
    else:
        print("[deps] All backend dependencies already installed.")


def ensure_frontend_dependencies():
    if (FRONTEND_DIR / "node_modules").exists():
        print("[frontend] node_modules already present.")
        return
    print("[frontend] Installing frontend dependencies (npm install)...")
    subprocess.run([NPM_CMD, "install"], cwd=FRONTEND_DIR, check=True)


def main():
    ensure_single_venv()
    ensure_backend_dependencies()
    ensure_frontend_dependencies()

    print("\n[backend] Starting FastAPI on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [str(VENV_PYTHON), "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        cwd=BACKEND_DIR,
    )

    time.sleep(2)

    print("[frontend] Starting Vite dev server on http://localhost:5173 ...")
    frontend_proc = subprocess.Popen([NPM_CMD, "run", "dev"], cwd=FRONTEND_DIR)

    time.sleep(3)
    webbrowser.open("http://localhost:5173")

    print("\nBoth servers are running. Press Ctrl+C to stop both.\n")
    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("[backend] process exited unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("[frontend] process exited unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        for proc in (backend_proc, frontend_proc):
            if proc.poll() is None:
                proc.terminate()
        for proc in (backend_proc, frontend_proc):
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    sys.exit(main())
