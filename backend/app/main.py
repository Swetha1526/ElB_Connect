# backend/app/main.py
import os
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.database.connection import init_db
from backend.app.database.seed_data import seed_database
from backend.app.routes import (
    applications_router,
    inspections_router,
    meters_router,
    grievances_router,
    stats_router
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_database(force=False)
    yield

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Full-stack REST API for Electricity Board Connections, Feasibility Audits, Smart Meter Registry & Power Outage Grievances.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected server error occurred. Please check backend logs or try again.",
            "detail": str(exc) if settings.DEBUG else None
        }
    )

# Register API Routers
app.include_router(stats_router, prefix=settings.API_V1_PREFIX)
app.include_router(applications_router, prefix=settings.API_V1_PREFIX)
app.include_router(inspections_router, prefix=settings.API_V1_PREFIX)
app.include_router(meters_router, prefix=settings.API_V1_PREFIX)
app.include_router(grievances_router, prefix=settings.API_V1_PREFIX)

# Health Check & Root Info Endpoints
@app.get("/health", tags=["System Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "VoltFlow Electricity Board Management System",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.get("/api", tags=["System Health"])
def api_info():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "documentation": "/docs",
        "endpoints": {
            "applications": f"{settings.API_V1_PREFIX}/applications",
            "inspections": f"{settings.API_V1_PREFIX}/inspections",
            "meters": f"{settings.API_V1_PREFIX}/meters",
            "grievances": f"{settings.API_V1_PREFIX}/grievances",
            "stats": f"{settings.API_V1_PREFIX}/stats/dashboard"
        }
    }

# Mount Frontend static files if directory exists
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    if (FRONTEND_DIR / "css").exists():
        app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
    if (FRONTEND_DIR / "js").exists():
        app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")
    if (FRONTEND_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend_root():
        index_path = FRONTEND_DIR / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {
            "message": "Welcome to VoltFlow API. Visit /docs for Swagger UI documentation."
        }
