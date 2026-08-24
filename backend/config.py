"""
Configuration and Environment Loader (SIH-36)
Automatically loads .env from project root without external dependencies.
"""

import os
from pathlib import Path

# Locate root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

def load_env_file(env_path: Path = ENV_PATH):
    """Parses .env key-value pairs into os.environ if not already set."""
    if not env_path.exists():
        return
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

# Auto-load on import
load_env_file()

# Centralized settings
DATAGOV_API_KEY = os.environ.get("DATAGOV_API_KEY", "")
DATAGOV_BASE_URL = "https://api.data.gov.in/resource"
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
PORT = int(os.environ.get("PORT", 5000))
FLASK_ENV = os.environ.get("FLASK_ENV", "production")
