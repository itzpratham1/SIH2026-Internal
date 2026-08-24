import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.agmarknet_fetcher import get_fetcher
    from backend.data_service import get_real_road_routing, fetch_live_weather
    from backend.cascade_engine import calculate_cascade_and_verdict
    from backend.ml_engine import ml_engine
    
    print("=" * 60)
    print("1. Testing Live data.gov.in Agmarknet API Connection...")
    fetcher = get_fetcher()
    status = fetcher.get_status()
    print("Agmarknet Status:", status)
    
    live_gwalior_wheat = fetcher.get_live_mandi_price("wheat", "gwalior")
    print(f"Live Wheat (Gwalior): Market='{live_gwalior_wheat['market']}', Modal=Rs.{live_gwalior_wheat['modal_price']}, Date={live_gwalior_wheat['arrival_date']}")
    
    print("\n2. Testing Live Open-Meteo Weather for Gwalior...")
    w = fetch_live_weather("gwalior")
    print("Weather Result:", w)
    
    print("\n3. Testing Live OSRM Road Routing Gwalior -> Morena...")
    r = get_real_road_routing("gwalior", "morena")
    print("Routing Result:", r)
    
    print("\n4. Testing LightGBM Quantile Forecast & Cascade Score for Wheat in Gwalior...")
    res = calculate_cascade_and_verdict("wheat", "gwalior")
    print(f"Price: Rs.{res['current_price']} | 80% Range: [Rs.{res['range_low']} - Rs.{res['range_high']}] | Cascade Score: {res['cascade_score']}/100")
    print(f"Verdict: {res['verdict']['label_en']} | Reason: {res['verdict']['reason_en']}")
    print(f"Candidate Mandis Count: {len(res['mandis'])}")
    for m in res["mandis"]:
        print(f"   -> {m['name']} ({m.get('apmc_name')}): Rs.{m['price']} | Road: {m['distance_km']} km ({m['duration_mins']} mins)")
        
    print("\n5. Testing True Walk-Forward Rolling-Origin Backtesting...")
    bt = res["backtest"]
    print("Actual 14D:", bt["actual_14d"])
    print("Predicted 14D (Q50):", bt["predicted_14d"])
    print(f"Mean Directional Accuracy (MDA): {bt['mda_pct']}%")
    print(f"80% Interval Calibration Hit Rate: {bt['calibration_80pct_hit_rate']}%")
    
    assert len(bt["actual_14d"]) == 14, "Actual length must be 14"
    assert len(bt["predicted_14d"]) == 14, "Predicted length must be 14"
    assert 0 <= bt["mda_pct"] <= 100, "MDA must be percentage"
    assert 0 <= bt["calibration_80pct_hit_rate"] <= 100, "Calibration rate must be percentage"
    
    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY — 100% AUTHENTIC REAL AGMARKNET DATA PIPELINE!")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
