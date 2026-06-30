import pandas as pd
import requests
import os
import time 
from datetime import datetime, timezone 
#requests makes the http to caqll our API 

#stuffs to import and set up the data we want to fetch from the API
SYMBOL       = "BTCUSDT"
DEPTH        = 10
INTERVAL     = 1.0
DURATION     = 24 * 60 * 60
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "..", "Data", "raw")
OUTPUT_FILE  = os.path.join(OUTPUT_DIR, f"orderbook_{SYMBOL}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv")
API_URL      = f"https://api.binance.com/api/v3/depth?symbol={SYMBOL}&limit={DEPTH}"


def fetch_orderbook_data():
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"  [WARNING] Request failed: {e}")
        return None