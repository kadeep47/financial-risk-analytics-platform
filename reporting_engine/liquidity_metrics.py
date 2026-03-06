import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.utils.io import load_dataframe, save_dataframe

def calculate_lcr(cashflows: pd.DataFrame, instruments: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates a proxy for Liquidity Coverage Ratio (LCR)
    LCR = High-Quality Liquid Assets (HQLA) / Total Net Cash Outflows over 30 days
    Here we simulate it using 30-day bucket inflows/outflows.
    """
    df = pd.merge(cashflows, instruments[['instrument_id', 'instrument_type']], on='instrument_id', how='left')
    
    # Very basic: anything with 'period_1' (representing the first month)
    short_term = df[df['date'] == 'period_1'].copy()
    
    inflows = short_term[short_term['instrument_type'].isin(['loan', 'bond'])]['total_amount'].sum()
    outflows = short_term[short_term['instrument_type'] == 'deposit']['total_amount'].sum()
    
    # Assume static HQLA for simulation purposes
    hqla = 50000.0 
    
    net_outflows = max(0, outflows - min(inflows, 0.75 * outflows)) # 75% cap rule simplified
    lcr = (hqla / net_outflows) if net_outflows > 0 else float('inf')
    
    report = pd.DataFrame([{
        "Metric": "Liquidity Coverage Ratio (LCR)",
        "HQLA": hqla,
        "Net Outflows (30D)": net_outflows,
        "Ratio": lcr
    }])
    return report

def calculate_nsfr(instruments: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates a proxy for Net Stable Funding Ratio (NSFR)
    NSFR = Available Stable Funding (ASF) / Required Stable Funding (RSF)
    """
    # Simplifying: Retail deposits have high ASF weight, Corporate lower.
    asf = 0
    rsf = 0
    
    for _, row in instruments.iterrows():
        if row['instrument_type'] == 'deposit':
            weight = 0.9 if row['customer_segment'] == 'retail' else 0.5
            asf += row['notional'] * weight
        elif row['instrument_type'] == 'loan':
            weight = 0.85 if row['customer_segment'] == 'retail' else 1.0 # Requires more funding
            rsf += row['notional'] * weight
        elif row['instrument_type'] == 'bond':
            rsf += row['notional'] * 0.5 # moderately liquid
            
    nsfr = asf / rsf if rsf > 0 else float('inf')
    
    report = pd.DataFrame([{
        "Metric": "Net Stable Funding Ratio (NSFR)",
        "ASF": asf,
        "RSF": rsf,
        "Ratio": nsfr
    }])
    return report

def generate_reports():
    print("Generating Liquidity Reports...")
    try:
        cashflows = load_dataframe("data/processed/cashflows.parquet", format="parquet")
        instruments = load_dataframe("data/processed/clean_instruments.parquet", format="parquet")
    except Exception:
        cashflows = load_dataframe("data/processed/cashflows.csv", format="csv")
        instruments = load_dataframe("data/raw/raw_instruments.csv", format="csv")
        
    lcr_df = calculate_lcr(cashflows, instruments)
    nsfr_df = calculate_nsfr(instruments)
    
    save_dataframe(lcr_df, "data/processed/liquidity_report.csv", format="csv")
    save_dataframe(nsfr_df, "data/processed/nsfr_report.csv", format="csv")
    
    print("Reports generated: liquidity_report.csv, nsfr_report.csv")
    print("\n--- LCR ---")
    print(lcr_df)
    print("\n--- NSFR ---")
    print(nsfr_df)

if __name__ == "__main__":
    generate_reports()
