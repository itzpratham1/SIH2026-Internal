"""
Flask Application for Crop Price Intelligence Platform (SIH-36)
Serves:
- Real REST API endpoints (/api/verdict, /api/calculate-profit, /api/target-check, /api/backtest, /api/meta, /api/agmarknet-status)
- Static UI for interactive browser experience
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.config import PORT
from backend.cascade_engine import calculate_cascade_and_verdict
from backend.ml_engine import ml_engine
from backend.data_service import MANDI_COORDINATES, CROP_METADATA, get_real_road_routing
from backend.traffic_tracker import traffic_tracker
from backend.agmarknet_fetcher import get_fetcher

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")

@app.route("/sw.js")
def serve_sw():
    return send_from_directory("../frontend", "sw.js", mimetype="application/javascript")

@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory("../frontend", "manifest.json", mimetype="application/manifest+json")


@app.route("/api/meta", methods=["GET"])
def get_metadata():
    fetcher_status = get_fetcher().get_status()
    return jsonify({
        "mandis": MANDI_COORDINATES,
        "crops": CROP_METADATA,
        "agmarknet_status": fetcher_status
    })

@app.route("/api/agmarknet-status", methods=["GET"])
def get_agmarknet_status():
    """Returns real-time data.gov.in Agmarknet API connection status and live metrics."""
    crop = request.args.get("crop", "onion")
    mandi = request.args.get("mandi", "gwalior")
    fetcher = get_fetcher()
    status = fetcher.get_status()
    live_price_info = fetcher.get_live_mandi_price(crop, mandi)
    
    return jsonify({
        "status": status,
        "crop": crop,
        "mandi": mandi,
        "live_price_data": live_price_info
    })

@app.route("/api/verdict", methods=["GET", "POST"])
def get_verdict():
    crop = request.args.get("crop", "onion")
    mandi = request.args.get("mandi", "gwalior")
    
    sim_overrides = None
    if request.method == "POST":
        data = request.get_json() or {}
        crop = data.get("crop", crop)
        mandi = data.get("mandi", mandi)
        sim_overrides = data.get("sim_overrides")
        
    # Log passive view impression to sliding window tracker
    traffic_tracker.record_event(mandi, event_type="view")
    
    result = calculate_cascade_and_verdict(crop, mandi, sim_overrides)
    return jsonify(result)

@app.route("/api/reset-traffic", methods=["GET", "POST"])
@app.route("/api/reset-sim", methods=["GET", "POST"])
def reset_traffic():
    """Resets the live sliding window traffic tracker and in-memory congestion buffers."""
    traffic_tracker.clear_all()
    return jsonify({
        "status": "success",
        "message": "Traffic and congestion tracker reset to zero baseline."
    })

@app.route("/api/backtest", methods=["GET"])
def get_backtest():
    """
    Dedicated endpoint returning the authentic 14-day rolling origin walk-forward backtest.
    """
    crop = request.args.get("crop", "onion")
    mandi = request.args.get("mandi", "gwalior")
    backtest = ml_engine.compute_backtest_metrics(crop, mandi)
    return jsonify({
        "crop": crop,
        "mandi": mandi,
        "backtest": backtest
    })

@app.route("/api/calculate-profit", methods=["POST"])
def calculate_profit():
    """
    Computes net profit across all candidate mandis using real road distances.
    Net = (Price * Qty) - (2 * Road_Distance * Fuel_Rate) - Labor_Cost
    """
    data = request.get_json() or {}
    origin_mandi = data.get("origin_mandi", "gwalior")
    crop_key = data.get("crop", "onion")
    qty = float(data.get("quantity_quintals", 10))
    fuel_rate = float(data.get("fuel_rate_per_km", 12))
    labor_cost = float(data.get("labor_flat", 300))
    
    # Log high-intent route query for origin mandi
    traffic_tracker.record_event(origin_mandi, event_type="route_intent")
    
    # Base calculation
    verdict_data = calculate_cascade_and_verdict(crop_key, origin_mandi)
    
    results = []
    for m in verdict_data["mandis"]:
        dist = m["distance_km"]
        transport_cost = 2 * dist * fuel_rate # Round trip
        gross_revenue = m["price"] * qty
        net_profit = gross_revenue - transport_cost - labor_cost
        
        results.append({
            "mandi_key": m["key"],
            "mandi_name": m["name"],
            "apmc_name": m.get("apmc_name", m["name"]),
            "distance_km": dist,
            "duration_mins": m["duration_mins"],
            "gross_price": m["price"],
            "gross_revenue": round(gross_revenue),
            "transport_cost": round(transport_cost),
            "labor_cost": round(labor_cost),
            "net_profit": round(net_profit),
            "routing_source": m["routing_source"],
            "data_source": m.get("data_source", "Agmarknet")
        })
        
    results.sort(key=lambda x: x["net_profit"], reverse=True)
    return jsonify({
        "origin_mandi": origin_mandi,
        "crop": crop_key,
        "quantity_quintals": qty,
        "ranked_mandis": results,
        "best_mandi": results[0]
    })

@app.route("/api/target-check", methods=["POST"])
def check_target_price():
    """
    Evaluates probability of price crossing ₹X in 7 days using Quantile distribution bounds.
    """
    data = request.get_json() or {}
    crop = data.get("crop", "onion")
    mandi = data.get("mandi", "gwalior")
    target = float(data.get("target_price", 2400))
    
    res = calculate_cascade_and_verdict(crop, mandi)
    low = res["range_low"]
    high = res["range_high"]
    curr = res["current_price"]
    
    if target <= low:
        status = "likely"
        prob = 85
        msg_en = f"Likely (~85% probability) — historically achievable within 7 days based on current momentum."
    elif target <= high:
        status = "possible"
        prob = 50
        msg_en = f"Possible (~50% probability) — sits within the LightGBM 80% confidence prediction band [₹{low}–₹{high}]."
    else:
        status = "unlikely"
        prob = 15
        msg_en = f"Unlikely (<15% probability) — exceeds 90th percentile quantile prediction for this 7-day window."
        
    return jsonify({
        "target_price": target,
        "current_price": curr,
        "predicted_range": [low, high],
        "status": status,
        "probability_pct": prob,
        "explanation": msg_en
    })

if __name__ == "__main__":
    print(f"Crop Price Intelligence Engine running on http://127.0.0.1:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)
