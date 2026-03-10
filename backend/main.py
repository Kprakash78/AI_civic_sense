"""
main.py
-------
FastAPI application entrypoint for the Rakshita backend.

• Mounts /static for frontend assets (Vanilla JS / Chart.js).
• Includes API routers for complaints and auth.
• Creates DB tables on startup.
• Configures CORS middleware.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from db.database import engine, Base
from api.routes_complaints import router as complaints_router
from api.routes_auth import router as auth_router


# ── Lifespan: create tables on startup ────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all ORM tables (dev convenience – use Alembic in production)."""
    Base.metadata.create_all(bind=engine)
    yield


# ── App instance ──────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description=(
        "Rakshita – AI-driven civic grievance prioritisation engine. "
        "Replaces FIFO ticket queues with severity + credibility scoring."
    ),
    lifespan=lifespan,
)


# ── CORS ──────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Static files ──────────────────────────────────────────

static_dir = Path(__file__).resolve().parent / "static"
if static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")


# ── Routers ───────────────────────────────────────────────

app.include_router(complaints_router)
app.include_router(auth_router)


# ── Health check ──────────────────────────────────────────

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
