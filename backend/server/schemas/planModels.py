from pydantic import BaseModel, PositiveFloat, NonNegativeFloat
from datetime import date
from typing import Optional, Literal, Dict, List

class PlanningInput(BaseModel):
    income: PositiveFloat
    expenses: PositiveFloat
    liquid_savings: NonNegativeFloat

class PlanningSnapshot(BaseModel):
    savings_rate: float
    monthly_buffer: float
    runway_months: float
    pressure_level: Literal["low", "medium", "high"]

class EconomicSignal(BaseModel):
    trend_direction: str
    latest_value: float
    mom_pct_change: Optional[float] = None
    yoy_pct_change: Optional[float] = None
    as_of_date: date

class PlanningInsight(BaseModel):
    headline: str
    explanation: str
    severity: Literal["low", "medium", "high"]
    as_of_date: date

class PlanningResponse(BaseModel):
    snapshot: PlanningSnapshot
    signals: Dict[str, EconomicSignal]
    insights: List[PlanningInsight]

