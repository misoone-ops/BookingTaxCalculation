
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

class ExtractedData(BaseModel):
    source: str
    gross: Optional[float] = None
    commission: Optional[float] = None
    payout: Optional[float] = None
    nights: Optional[int] = None
    guests: Optional[int] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('gross', 'commission', 'payout', mode='before')
    @classmethod
    def comma_to_dot(cls, v):
        if isinstance(v, str):
            v = v.strip().replace(' ', '').replace('.', '').replace(',', '.')
            try:
                return float(v)
            except:
                return None
        return v

class CalculationRules(BaseModel):
    currency: str = "EUR"
    booking_commission_pct: float = 0.0
    iva_pct: float = 0.0
    withholding_tax_pct: float = 0.0
    cleaning_fee_fixed: float = 0.0
    other_fixed_costs: float = 0.0
    city_tax_per_person_per_night: float = 0.0

class CalculationResult(BaseModel):
    currency: str
    gross_total: float
    computed_commission: float
    iva_amount: float
    city_tax_total: float
    fixed_costs_total: float
    net_total: float
    details: Dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
