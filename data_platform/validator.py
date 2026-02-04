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
                data_dict['start_date'] = data_dict['start_date'].date()
            elif isinstance(data_dict['start_date'], str):
                data_dict['start_date'] = pd.to_datetime(data_dict['start_date']).date()
                
            if isinstance(data_dict['maturity_date'], pd.Timestamp):
                data_dict['maturity_date'] = data_dict['maturity_date'].date()
            elif isinstance(data_dict['maturity_date'], str):
                data_dict['maturity_date'] = pd.to_datetime(data_dict['maturity_date']).date()
                
            validated = Instrument(**data_dict)
            valid_records.append(validated.model_dump())
        except ValidationError as e:
            errors += 1
            print(f"Validation error at row {idx}: {e}")
            
    print(f"Validation complete: {len(valid_records)} valid, {errors} errors.")
    return pd.DataFrame(valid_records)

if __name__ == "__main__":
    from shared.utils.io import load_dataframe, save_dataframe
    df = load_dataframe("data/raw/raw_instruments.csv", format="csv")
    cleaned_df = validate_dataset(df)
    save_dataframe(cleaned_df, "data/processed/clean_instruments.parquet", format="parquet")
