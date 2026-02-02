import os
import uuid
import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import List, Dict

# Assumes we run this script from the workspace root or handles path logic.
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.schemas.instrument import Instrument

def generate_synthetic_data(num_records: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic financial instrument data and validate using Pydantic schema.
    """
    records: List[Dict] = []
    
    types = ["loan", "bond", "deposit"]
    frequencies = ["monthly", "quarterly"]
    segments = ["retail", "corporate"]
    
    # Statistical parameters for interest rates and notionals
    # Notional: log-normal distribution
    mu, sigma = 10.0, 1.5
    
    for _ in range(num_records * len(types)):
        inst_type = np.random.choice(types)
        
        # Interest rate follows normal distribution (mean=5%, std=2%) but clipped to positive
        rate = max(0.001, np.random.normal(loc=0.05, scale=0.02))
        
        # Notional follows log-normal distribution
        notional = float(np.random.lognormal(mean=mu, sigma=sigma))
        
        # Start date between 1 year ago and today
        start_days_ago = np.random.randint(0, 365)
        start_d = date.today() - timedelta(days=start_days_ago)
        
