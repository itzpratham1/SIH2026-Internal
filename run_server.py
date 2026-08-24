"""
One-Click Launcher for Crop Price Intelligence Platform (SIH-36)
"""

import sys
import os
import webbrowser
import threading
import time

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 65)
    print("  SMART INDIA HACKATHON 2026 -- SIH-36: CROP PRICE INTELLIGENCE")
    print("   Team NODE VI - Gwalior Cluster (Wheat, Onion, Tomato)")
    print("=" * 65)
    print("> Starting Flask Engine on http://127.0.0.1:5000 ...")
    
    # Launch browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
