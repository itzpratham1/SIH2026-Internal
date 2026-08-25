# 🌾 SIH-36: Crop Price Intelligence Platform
> **Smart India Hackathon 2026 — Team NODE VI**  
> *Target Region: Gwalior Cluster (Wheat, Onion, Tomato)*

An intelligent, ML-powered decision support system designed to help farmers optimize produce marketing timing, mandi routing, and cold storage decisions to maximize net profit.

---

## ⚡ 1-Click Quick Start (Easiest Way)

### 📥 Step 1: Download the Project
- **Option A (Download ZIP):** Click the green **Code** button on GitHub $\rightarrow$ **[Download ZIP]**, then extract the ZIP file.
- **Option B (Git Clone):**
  ```bash
  git clone https://github.com/itzpratham1/SIH2026.git
  cd SIH2026
  ```

---

### 🚀 Step 2: Run in One Click

#### 🖥️ Windows:
Simply **double-click** [`start.bat`](file:///d:/SIH/start.bat) (or run in CMD/PowerShell):
```bat
start.bat
```
*(This automatically creates the virtual environment, installs all packages, configures `.env`, starts the server, and opens your browser!)*

#### 🍎 macOS / Linux:
Open Terminal in the project folder and run:
```bash
chmod +x start.sh
./start.sh
```

#### 🐳 Docker (Optional):
```bash
docker compose up
```

The web dashboard will automatically open at **`http://localhost:5000`** (or `http://127.0.0.1:5000`).

---

## 🛠️ Manual Setup (Step-by-Step)

If you prefer setting up manually step-by-step:

1. **Prerequisites:** Python 3.10+ installed.
2. **Create & Activate Virtual Environment:**
   - *Windows:*
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - *macOS / Linux:*
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment File (Optional):**
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # macOS/Linux
   ```
5. **Start Application:**
   ```bash
   python run_server.py
   ```

---

## 🧪 Run Tests & Verification
Run the backend validation suite to verify ML models, routing calculations, and decision cascades:
```bash
python test_engine.py
```

---

## 📂 Project Structure

```
SIH/
├── backend/                  # Flask REST API & ML Decision Engines
│   ├── app.py                # Server entry point & API route handlers
│   ├── cascade_engine.py     # Decision cascade (Sell Now vs Hold vs Storage)
│   ├── ml_engine.py          # LightGBM & Time-Series forecasting models
│   ├── data_service.py       # Mandi geo-coordinates & routing engine
│   ├── agmarknet_fetcher.py  # Data.gov.in Agmarknet API integration
│   ├── traffic_tracker.py    # Mandi congestion & inflow tracking
│   └── config.py             # App configuration & environment loader
├── frontend/                 # Progressive Web App (PWA)
│   ├── index.html            # Core Single Page Application UI
│   ├── sw.js                 # Service Worker (Offline caching & PWA)
│   ├── manifest.json         # Web App Manifest
│   └── icon.svg              # App Icon
├── start.bat                 # 1-Click launcher for Windows
├── start.sh                  # 1-Click launcher for macOS / Linux
├── Dockerfile                # Docker container configuration
├── docker-compose.yml        # Docker Compose configuration
├── run_server.py             # Smart Python server launcher & browser opener
├── test_engine.py            # Automated test & verification suite
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

---

## 🌐 API Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/meta` | `GET` | Supported mandis, crop parameters, and Agmarknet API status |
| `/api/calculate-profit` | `POST` | Calculates net profit per mandi considering distance, fuel, and storage |
| `/api/verdict` | `POST` | Comprehensive ML prediction & marketing timing recommendation |
| `/api/target-check` | `POST` | Checks probability of hitting farmer's target price |
| `/api/backtest` | `GET` | Historical accuracy and model performance metrics |
| `/api/agmarknet-status` | `GET` | Agmarknet live sync health check |
