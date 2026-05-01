import pytest
import pandas as pd
from data_platform.generator import generate_synthetic_data
from shared.schemas.instrument import Instrument
from pydantic import ValidationError

def test_data_generation_counts():
    df = generate_synthetic_data(num_records=10)
    assert len(df) == 30 # 3 types * 10 
    assert "loan" in df['instrument_type'].unique()
    assert "bond" in df['instrument_type'].unique()

def test_data_schema_compliance():
    df = generate_synthetic_data(num_records=5)
    for _, row in df.iterrows():
        # Will throw ValidationError if schema is violated
        data_dict = row.to_dict()
        data_dict['start_date'] = data_dict['start_date'].date() if isinstance(data_dict['start_date'], pd.Timestamp) else data_dict['start_date']
        data_dict['maturity_date'] = data_dict['maturity_date'].date() if isinstance(data_dict['maturity_date'], pd.Timestamp) else data_dict['maturity_date']
        inst = Instrument(**data_dict)
        assert inst.notional > 0
