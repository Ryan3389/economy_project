from fastapi import APIRouter
# from server.controllers.planControllers import submit_plan_snapshot
from backend.server.controllers.planControllers import econ_context
from backend.server.schemas.planModels import PlanningResponse, PlanningInput
plan_router = APIRouter()

# @plan_router.post("/snapshot", response_model=PlanningResponse)
# def plan_snapshot(input: PlanningInput):
#     return submit_plan_snapshot(input)

@plan_router.get("/context")
def get_econ_context():
    return econ_context()