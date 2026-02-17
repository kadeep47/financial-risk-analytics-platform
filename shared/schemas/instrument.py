from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from datetime import date

class Instrument(BaseModel):
    """
    Unified Data Contract for Financial Instruments.
    """
    model_config = ConfigDict(strict=True)
