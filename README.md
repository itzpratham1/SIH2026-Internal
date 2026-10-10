# KrishiBhav — Crop Price Intelligence & Mandi Advisory Platform

**Smart India Hackathon 2026** | **Problem Statement: SIH-36**  
**Team NODE VI** | **Target Region: Gwalior Cluster, Madhya Pradesh** (*Wheat, Onion, Tomato*)

KrishiBhav is an offline-first agricultural decision support system designed to help smallholder farmers maximize net profit. By combining real-time mandi prices from Agmarknet, quantile machine learning price forecasting, a 9-factor cascade decision matrix, and road transport logistics, the platform guides farmers on optimal marketing timing, mandi selection, and storage feasibility.

---

## Key Capabilities

- **Live Agmarknet Data Pipeline**: Direct integration with the Open Government Data Portal (data.gov.in) to ingest daily modal prices, arrivals, and min/max ranges for Lashkar (Gwalior), Morena, Bhind, and Shivpuri APMC mandis.
- **Quantile Price Forecasting (LightGBM)**: Predicts 7-day price bounds across 10th, 50th, and 90th percentiles using causal feature engineering (lagged momentum, rainfall anomalies, and spatial neighbor leads). Validated via rolling-origin walk-forward backtesting (Mean Directional Accuracy).
- **9-Factor Cascade Risk Engine**: Computes a normalized 0–100 Cascade Score balancing price momentum, arrival pressure, perishable shelf life (ICAR guidelines), cold storage economics, and MSP safety floors to recommend *Sell Now*, *Hold*, or *Store*.
- **Net Farmer Realization & OSRM Routing**: Calculates real net returns per mandi after deducting round-trip vehicle fuel and labor costs, avoiding misleading gross price comparisons.
- **Mandi Congestion Safeguard**: Monitors collective routing queries in a sliding time window to prevent herd behavior and local market oversupply.
- **Offline-First Progressive Web App**: Built with vanilla HTML/CSS/JS and Service Workers for zero-dependency mobile access, featuring bilingual UI (Hindi and English) and audio speech readout.

---

## System Architecture

```
SIH/
├── backend/
│   ├── app.py                 # Flask REST API endpoints & route handlers
│   ├── ml_engine.py           # LightGBM quantile regression & backtesting
│   ├── cascade_engine.py      # 9-factor decision cascade & shelf-life logic
│   ├── agmarknet_fetcher.py   # data.gov.in Agmarknet API integration & caching
│   ├── data_service.py        # OSRM road routing, coordinates & weather service
│   ├── traffic_tracker.py     # Mandi congestion & inflow tracking
│   ├── historical_data.py     # Mandi price time-series provider
│   └── config.py              # Application configuration
├── frontend/
│   ├── index.html             # Single-page dashboard interface
│   ├── sw.js                  # Service Worker (offline caching)
│   ├── manifest.json          # Web App Manifest
│   └── icon.svg               # App icon
├── requirements.txt           # Python dependencies
├── run_server.py              # Local server launcher
├── test_engine.py             # Validation test suite
├── Dockerfile                 # Container setup
└── docker-compose.yml         # Container orchestration
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/itzpratham1/SIH2026-Internal.git
   cd SIH2026-Internal
   ```

2. **Create and activate a virtual environment**
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run_server.py
   ```
   The dashboard will be available at `http://localhost:5000`.

   *Alternatively, on Windows run `start.bat`, on Linux/macOS run `./start.sh`, or with Docker run `docker compose up`.*

---

## Verification & Testing

To run the verification suite covering the Agmarknet API connection, OSRM routing, LightGBM quantile forecasting, and rolling-origin backtest metrics:

```bash
python test_engine.py
```

---

## API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/meta` | `GET` | Supported mandis, crop metadata, and Agmarknet connection health |
| `/api/verdict` | `GET`, `POST` | Machine learning price forecasts and marketing timing recommendations |
| `/api/calculate-profit` | `POST` | Computes net profit per candidate mandi after transport and labor |
| `/api/target-check` | `POST` | Probability evaluation of price reaching a target threshold |
| `/api/backtest` | `GET` | 14-day rolling origin walk-forward performance metrics |
| `/api/agmarknet-status` | `GET` | Live mandi APMC auction sync status |
| `/api/reset-traffic` | `POST` | Resets in-memory mandi congestion counters |
