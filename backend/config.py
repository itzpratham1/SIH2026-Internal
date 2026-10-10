"""
Application Configuration (SIH-36)
"""

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

def load_env_file(env_path: Path = ENV_PATH):
    if not env_path.exists():
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key and key not in os.environ:
                        os.environ[key] = val
    except Exception:
        pass

load_env_file()

# Centralized settings with robust defaults
DATAGOV_API_KEY = os.environ.get("DATAGOV_API_KEY", "579b464db66ec23bdd000001239d985bbad24bf450ffabea18c811c2")
DATAGOV_BASE_URL = "https://api.data.gov.in/resource"
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
PORT = int(os.environ.get("PORT", 5000))
FLASK_ENV = os.environ.get("FLASK_ENV", "production")

