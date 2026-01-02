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
    if not os.path.exists(f"{build_dir}/engine"):
        print("Compiling C++ Cashflow Engine...")
        subprocess.run(["cmake", ".."], cwd=build_dir, check=True)
        subprocess.run(["make"], cwd=build_dir, check=True)

    print("Running C++ Engine...")
    executable = f"./{build_dir}/engine"
    subprocess.run([
        executable, 
        "data/processed/clean_instruments.csv",
        "data/processed/cashflows.csv"
    ], check=True)

    # Convert output back to parquet
    print("Converting outputs back to Parquet...")
    flows_df = load_dataframe("data/processed/cashflows.csv", format="csv")
    save_dataframe(flows_df, "data/processed/cashflows.parquet", format="parquet")
    print("Engine execution complete!")

if __name__ == "__main__":
    run_engine()
