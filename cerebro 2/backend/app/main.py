"""FastAPI application entry point for Cerebro."""
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, tasks, verification, war_room, insights, setup, dashboard
from journal.journal_api import router as journal_router
from journal.chatbot_api import router as chatbot_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Workflow accountability app for job seekers",
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"CORS origins loaded: {settings.cors_origins}")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(setup.router, prefix="/api/setup", tags=["setup"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(verification.router, prefix="/api/verification", tags=["verification"])
app.include_router(war_room.router, prefix="/api/war-room", tags=["war-room"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(journal_router)
app.include_router(chatbot_router)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.options("/{any_path:path}")
async def options_any(any_path: str):
    """Global OPTIONS handler for CORS preflight debugging."""
    return Response(status_code=200)


@app.get("/api/dashboard")
async def get_dashboard():
    """Mock dashboard data for frontend."""
    return {
        "jars": [
            {"color": "yellow", "count": 3},
            {"color": "blue", "count": 2},
            {"color": "purple", "count": 1},
            {"color": "red", "count": 0},
        ],
        "logicAgent": {"challenge": "Invert Binary Tree", "status": "completed"},
        "jobScout": {"sources": ["LinkedIn", "Indeed", "Glassdoor"], "applied": 5},
        "orbHistory": [
            {"date": "2026-01-10", "orbs": 2},
            {"date": "2026-01-11", "orbs": 1},
        ],
    }
