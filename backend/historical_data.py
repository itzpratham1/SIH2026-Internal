"""
Agmarknet Market Price Series & Historical Data (SIH-36)
Provides historical daily modal prices (₹/quintal) and daily arrival volumes (quintals)
for Gwalior, Morena, Bhind, and Shivpuri mandis in Madhya Pradesh via data.gov.in API.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.agmarknet_fetcher import load_agmarknet_historical_series as _fetch_real


def load_agmarknet_historical_series(crop_key, mandi_key, days=150):
    """
    Returns daily Agmarknet price and arrival data fetched from data.gov.in API.
    """
    return _fetch_real(crop_key, mandi_key, days)