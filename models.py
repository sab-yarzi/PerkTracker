from pydantic import BaseModel, Field
from typing import Optional, List

class SingularPerk(BaseModel):
    company_name: str
    offer_text: str = Field(..., description="Raw offer headline text")
    expiry_text: Optional[str] = None
    conditions_text: Optional[str] = None

    # Parsed fields (filled by your code, NOT the model)
    percentage_value: Optional[float] = None
    minimum_spend: Optional[float] = None
    money_back: Optional[float] = None
    cap_amount: Optional[float] = None

    confidence: float

class PerkList(BaseModel):
    perks: List[SingularPerk]
    overall_confidence: float