import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.utils.io import load_dataframe, save_dataframe

def calculate_lcr(cashflows: pd.DataFrame, instruments: pd.DataFrame) -> pd.DataFrame:
