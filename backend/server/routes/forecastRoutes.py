from fastapi import APIRouter
from backend.server.controllers.forecastControllers import economy_forecasts
from backend.server.schemas.forecastModels import ForecastRequest
forecast_router = APIRouter()

@forecast_router.post("/predict")
def forecasts(req: ForecastRequest):
    return economy_forecasts(req.horizon_months)

