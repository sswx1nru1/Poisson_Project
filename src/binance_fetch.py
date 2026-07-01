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
    
def parse_snapshot(raw: dict, timestamp: datetime):
    row = {
        "timestamp":      timestamp.isoformat(),
        "last_update_id": raw["lastUpdateId"],
    }
    bids = raw["bids"]
    asks = raw["asks"]
    for i in range(DEPTH):
        row[f"bid_price_{i+1}"] = float(bids[i][0]) if i < len(bids) else None
        row[f"bid_qty_{i+1}"]   = float(bids[i][1]) if i < len(bids) else None
        row[f"ask_price_{i+1}"] = float(asks[i][0]) if i < len(asks) else None
        row[f"ask_qty_{i+1}"]   = float(asks[i][1]) if i < len(asks) else None
    best_bid = float(bids[0][0]) if bids else None
    best_ask = float(asks[0][0]) if asks else None
    row["mid_price"] = (best_bid + best_ask) / 2 if (best_bid and best_ask) else None
    row["spread"]    = (best_ask - best_bid)      if (best_bid and best_ask) else None
    return row
