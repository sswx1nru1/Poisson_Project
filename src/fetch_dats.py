import pandas as pd
import os 

OUTPUT_DIR = os.path.join("data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "binance_btc_l2_10min.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

file_url = "https://datasets.tardis.dev/v1/samples/binance/incremental_book_L2/2024/03/01.csv.gz"

start_time = 1709265600000000  
end_time   = 1709266200000000
# 4:00 to 4:10

