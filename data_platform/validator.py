import pandas as pd
from typing import List
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.schemas.instrument import Instrument
from pydantic import ValidationError

def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates a pandas DataFrame against the Instrument Pydantic schema.
    Returns a cleaned DataFrame containing only valid records.
    """
    valid_records = []
    errors = 0
    
    # Iterate over rows as dictionaries
    for idx, row in df.iterrows():
        try:
            # Convert pandas timestamp to date if necessary
            data_dict = row.to_dict()
            if isinstance(data_dict['start_date'], pd.Timestamp):
