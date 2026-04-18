from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class StressScenario(BaseModel):
    model_config = ConfigDict(strict=True)
    
    deposit_runoff: float
    loan_default: float
    interest_rate_shock: float
