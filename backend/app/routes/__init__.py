# backend/app/routes/__init__.py
from backend.app.routes.applications import router as applications_router
from backend.app.routes.inspections import router as inspections_router
from backend.app.routes.meters import router as meters_router
from backend.app.routes.grievances import router as grievances_router
from backend.app.routes.stats import router as stats_router

__all__ = [
    "applications_router",
    "inspections_router",
    "meters_router",
    "grievances_router",
    "stats_router"
]
