from fastapi import FastAPI

from backend.server.routes.economyRoutes import economy_router
from backend.server.routes.planRoutes import plan_router
from backend.server.routes.forecastRoutes import forecast_router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

app.include_router(economy_router, prefix="/api/economy")
app.include_router(plan_router, prefix="/api/planning")
app.include_router(forecast_router, prefix="/api/forecast")


DIST_DIR = Path(__file__).resolve().parents[2] / "client" / "dist"
ASSETS_DIR = DIST_DIR / "assets"


if DIST_DIR.exists():
    if ASSETS_DIR.exists():
        app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

    @app.get("/{full_path:path}")
    def spa_fallback(full_path: str):
        index_file = DIST_DIR / "index.html"
        return FileResponse(str(index_file))
