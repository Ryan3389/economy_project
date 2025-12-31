from pydantic import BaseModel

class ForecastRequest(BaseModel):
    horizon_months: int
