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
