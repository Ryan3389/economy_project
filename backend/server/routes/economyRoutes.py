from fastapi import APIRouter
from server.controllers.economyControllers import get_economy_summary, get_metric_trends, get_economy_insights
# from controllers.economyControllers import get_economy_summary, get_metric_trends, get_economy_insights
from server.schemas.economyModels import EconomySummaryItem, EconomyTrendResponse, EconomyInsights
# from schemas.economyModels import EconomySummaryItem, EconomyTrendResponse, EconomyInsights
economy_router = APIRouter()


@economy_router.get("/summary", response_model=list[EconomySummaryItem])
def economy_summary():
    return get_economy_summary()


@economy_router.get("/trends/{slug}", response_model=EconomyTrendResponse)
def economy_trends(slug:str, limit:int=60):
    return get_metric_trends(slug, limit)


@economy_router.get("/insight", response_model=EconomyInsights)
def economy_insights():
    return get_economy_insights()
