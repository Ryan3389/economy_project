from pydantic import BaseModel
from datetime import date


class EconomyMetricTrends(BaseModel):
    date: date
    value: float
    rolling_3m_avg: float | None
    rolling_12m_avg: float | None

class EconomyTrendResponse(BaseModel):
    metric: str
    data: list[EconomyMetricTrends]



class EconomySummaryItem(BaseModel):
    metric_name: str
    as_of_date: date
    latest_value: float
    mom_pct_change: float | None
    yoy_pct_change: float | None
    trend_direction: str
    summary: str

class EconomySummaryResponse(BaseModel):
    data: list[EconomySummaryItem]


# QUESTION: Why do we use [str, str] twice when there are three metrics
class EconomyInsights(BaseModel):
    headline: str
    explanation: str
    as_of_date: date
# class EconomyInsights(BaseModel):
#     title: str
#     message: str
#     drivers: dict[str, str]

