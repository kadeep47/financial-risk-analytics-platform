from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from datetime import date

class Instrument(BaseModel):
    """
    Unified Data Contract for Financial Instruments.
    """
    model_config = ConfigDict(strict=True)

    instrument_id: str
    instrument_type: Literal["loan", "bond", "deposit"]
    notional: float = Field(gt=0, description="Principal amount")
    interest_rate: float = Field(description="Annualised interest rate in decimals (e.g., 0.05 for 5%)")
    start_date: date
    maturity_date: date
    payment_frequency: Literal["monthly", "quarterly"]
    customer_segment: Literal["retail", "corporate"]
