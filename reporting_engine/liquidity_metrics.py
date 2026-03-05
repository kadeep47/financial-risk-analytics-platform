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
