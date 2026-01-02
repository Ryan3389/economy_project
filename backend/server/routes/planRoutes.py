from fastapi import APIRouter

from backend.server.controllers.planControllers import econ_context
from backend.server.schemas.planModels import PlanningResponse, PlanningInput
plan_router = APIRouter()



@plan_router.get("/context")
def get_econ_context():
    return econ_context()