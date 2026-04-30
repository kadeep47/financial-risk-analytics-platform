import pytest
import pandas as pd
from data_platform.generator import generate_synthetic_data
from shared.schemas.instrument import Instrument
from pydantic import ValidationError

def test_data_generation_counts():
    df = generate_synthetic_data(num_records=10)
    assert len(df) == 30 # 3 types * 10 
    assert "loan" in df['instrument_type'].unique()
