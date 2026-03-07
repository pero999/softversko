"""Glavna FastAPI aplikacija."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.database import create_db_and_tables
from app.routes.users import router as users_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle eventi aplikacije."""
    # Startup: kreiraj tablice
    create_db_and_tables()
    yield
    # Shutdown: cleanup ako treba


app = FastAPI(
    title=settings.app_name,
    description="FastAPI REST API s SQLModel i SQLite",
    version="0.1.0",
    lifespan=lifespan,
)

# Uključi rute
app.include_router(users_router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Dobrodošli u Softversko API!", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
