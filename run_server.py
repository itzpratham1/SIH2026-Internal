"""
One-Click Launcher for Crop Price Intelligence Platform (SIH-36)
Smart India Hackathon 2026 -- Team NODE VI
"""

import sys
import os
import shutil
import socket
import webbrowser
import threading
import time

# Ensure root directory is on Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

# 1. Check for critical dependencies
REQUIRED_PACKAGES = ["flask", "flask_cors", "pandas", "numpy", "scipy", "sklearn", "lightgbm"]
missing = []
for pkg in REQUIRED_PACKAGES:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"[!] Missing required Python packages: {', '.join(missing)}")
    print("[*] Auto-installing missing dependencies from requirements.txt...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(ROOT_DIR, "requirements.txt")])
        print("[+] Dependencies successfully installed!\n")
    except Exception as e:
        print(f"[ERROR] Could not auto-install dependencies: {e}")
        print("Please run manually: pip install -r requirements.txt\n")

from backend.app import app

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def open_browser(port=5000):
    time.sleep(1.2)
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = int(os.environ.get("PORT", 5000))

    print("\n" + "=" * 68)
    print("   SMART INDIA HACKATHON 2026 -- SIH-36: CROP PRICE INTELLIGENCE")
    print("   Target Region: Gwalior Cluster (Wheat, Onion, Tomato)")
    print("=" * 68)
    print(f"\n  Dashboard URL:   http://127.0.0.1:{port}")
    print(f"  Network Access:  http://{local_ip}:{port}")
    print("=" * 68 + "\n")
    print("Press Ctrl+C in this terminal to stop the server at any time.\n")

    # Launch browser automatically
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)


