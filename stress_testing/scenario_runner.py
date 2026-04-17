import json
import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stress_testing.models import StressScenario
from reporting_engine.liquidity_metrics import calculate_lcr
from shared.utils.io import load_dataframe

def apply_stress(cashflows: pd.DataFrame, instruments: pd.DataFrame, scenario: StressScenario) -> (pd.DataFrame, pd.DataFrame):
    """
    Applies stress parameters to the datasets, returning stressed copies.
    """
    cf_stressed = cashflows.copy()
    inst_stressed = instruments.copy()
    
    # Apply loan defaults to inflows
    # Finding loan instrument_ids
    loan_ids = inst_stressed[inst_stressed['instrument_type'] == 'loan']['instrument_id']
    deposit_ids = inst_stressed[inst_stressed['instrument_type'] == 'deposit']['instrument_id']
    
    # Haircut on cashflows from loans based on default rate
    cf_stressed.loc[cf_stressed['instrument_id'].isin(loan_ids), 'total_amount'] *= (1 - scenario.loan_default)
    
    # Increase outflows for deposits based on run-off rate
    cf_stressed.loc[cf_stressed['instrument_id'].isin(deposit_ids), 'total_amount'] *= (1 + scenario.deposit_runoff)
    
    # Extremely simplified interest rate shock (impacts next periods by reducing net present value/rates, but structurally we'll leave as simple run-off implementation for now)
    
    return cf_stressed, inst_stressed

def run_scenarios():
    print("Running Stress Scenarios...")
    
    with open("shared/configs/scenarios.json", "r") as f:
        config = json.load(f)
        
    try:
        cashflows = load_dataframe("data/processed/cashflows.parquet", format="parquet")
        instruments = load_dataframe("data/processed/clean_instruments.parquet", format="parquet")
    except Exception:
        cashflows = load_dataframe("data/processed/cashflows.csv", format="csv")
        instruments = load_dataframe("data/processed/clean_instruments.csv", format="csv")

    results = {}
    
    for name, params in config.items():
        scenario = StressScenario(**params)
        cf_s, inst_s = apply_stress(cashflows, instruments, scenario)
        
        # Calculate impacts
        lcr_report = calculate_lcr(cf_s, inst_s)
        
        results[name] = {
            "lcr_proxy": lcr_report['Ratio'].iloc[0],
            "net_outflows": lcr_report['Net Outflows (30D)'].iloc[0]
        }
        print(f"Scenario '{name}' -> LCR Proxy: {results[name]['lcr_proxy']:.2f}, Net Outflows: {results[name]['net_outflows']:.2f}")

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/stress_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("Stress test complete. Results saved to data/processed/stress_results.json")

if __name__ == "__main__":
    run_scenarios()
