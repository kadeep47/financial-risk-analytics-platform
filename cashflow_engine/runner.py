import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.utils.io import load_dataframe, save_dataframe

def run_engine():
    print("Preparing cashflow engine inputs...")
    # Read Parquet to CSV for the C++ engine
    try:
        df = load_dataframe("data/processed/clean_instruments.parquet", format="parquet")
    except Exception:
        df = load_dataframe("data/raw/raw_instruments.csv", format="csv")

    save_dataframe(df, "data/processed/clean_instruments.csv", format="csv")

    build_dir = "cashflow_engine/build"
    os.makedirs(build_dir, exist_ok=True)
    
    # We compile the cmake here strictly if the executable doesn't exist
