from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.api import hands, training, stats

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A learning tool for memorising poker hands and optimal play",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://diogopoletti.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    init_db()


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.app_name}


# Include API routers
app.include_router(hands.router, prefix="/api/hands", tags=["Hands"])
app.include_router(training.router, prefix="/api/training", tags=["Training"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])
