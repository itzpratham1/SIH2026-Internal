"""
In-Memory Sliding Window Mandi Traffic & Inflow Tracker (SIH-36)
- Tracks live timestamped impressions and high-intent route queries.
- Applies a probabilistic conversion model (Views: 30%, Transport lookups: 85%).
- Automatically prunes events older than 60 minutes (rolling 1-hour window).
"""

import time
import threading
from typing import Dict, List, Tuple

class MandiTrafficTracker:
    def __init__(self, window_seconds: int = 3600):
        self.window_seconds = window_seconds
        # Stores list of tuples: (timestamp, event_type, weight)
        self._events: Dict[str, List[Tuple[float, str, float]]] = {}
        self._lock = threading.Lock()
        
        # Event weights
        self.WEIGHT_PASSIVE_VIEW = 0.30       # 30% conversion probability for passive advisory views
        self.WEIGHT_ROUTE_INTENT = 0.85       # 85% conversion probability for active transport calculation

    def _prune_expired(self, current_time: float):
        cutoff = current_time - self.window_seconds
        for mandi in list(self._events.keys()):
            self._events[mandi] = [
                e for e in self._events[mandi] if e[0] >= cutoff
            ]

    def record_event(self, mandi_key: str, event_type: str = "view") -> None:
        """
        Records an interaction event for a given mandi.
        event_type: 'view' (passive impression) or 'route_intent' (transport lookup)
        """
        now = time.time()
        weight = self.WEIGHT_ROUTE_INTENT if event_type == "route_intent" else self.WEIGHT_PASSIVE_VIEW
        
        with self._lock:
            if mandi_key not in self._events:
                self._events[mandi_key] = []
            
            # Cap nominal passive browsing to realistic baseline (<= 10/hr)
            # Emergency congestion (>25/hr) is actively triggered via the Scenario Simulator
            current_inflow = sum(e[2] for e in self._events[mandi_key])
            if current_inflow < 10.0:
                self._events[mandi_key].append((now, event_type, weight))
            self._prune_expired(now)

    def get_mandi_metrics(self, mandi_key: str) -> dict:
        """
        Returns real-time 60-minute window statistics for a mandi.
        """
        now = time.time()
        with self._lock:
            self._prune_expired(now)
            events = self._events.get(mandi_key, [])
            
            raw_views = sum(1 for e in events if e[1] == "view")
            raw_routes = sum(1 for e in events if e[1] == "route_intent")
            
            # Expected inflow arrivals (probabilistic sum rounded to 1 decimal)
            expected_inflow = sum(e[2] for e in events)
            
            return {
                "raw_views": raw_views,
                "raw_route_intents": raw_routes,
                "total_interactions": len(events),
                "expected_inflow": round(expected_inflow, 1),
                "effective_farmer_count": int(round(expected_inflow))
            }

    def clear_all(self):
        """Clears in-memory buffer (useful for test resets)."""
        with self._lock:
            self._events.clear()

# Global singleton instance
traffic_tracker = MandiTrafficTracker(window_seconds=3600)
