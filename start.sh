#!/usr/bin/env bash
# =====================================================================
#    SMART INDIA HACKATHON 2026 -- SIH-36: CROP PRICE INTELLIGENCE
#              Team NODE VI - Gwalior Cluster Platform
# =====================================================================

set -e

# Detect Python 3 command
if command -v python3 &>/dev/null; then
    PY_CMD=python3
elif command -v python &>/dev/null; then
    PY_CMD=python
else
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/ or your package manager."
    exit 1
fi

echo "====================================================================="
echo "   SMART INDIA HACKATHON 2026 -- SIH-36: CROP PRICE INTELLIGENCE"
echo "             Team NODE VI - Gwalior Cluster Platform"
echo "====================================================================="
echo ""


# Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment (venv)..."
    $PY_CMD -m venv venv
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Install / update requirements
echo "[*] Checking and installing dependencies..."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

echo ""
echo "[*] Starting Application Server & Opening Browser..."
echo "====================================================================="
python run_server.py
