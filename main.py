"""Glavna FastAPI aplikacija - Sustav narudžbi za menzu."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.database import create_db_and_tables
from app.routes.auth import router as auth_router
from app.routes.menu import router as menu_router
from app.routes.orders import router as orders_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle eventi aplikacije."""
    # Startup: kreiraj tablice
    create_db_and_tables()
    yield
    # Shutdown: cleanup ako treba


app = FastAPI(
    title="Menza API",
    description="""
## Sustav narudžbi za menzu/kuhinju

### Funkcionalnosti:
- 🍽️ **Javni jelovnik** - pregled dostupnih jela
- 📝 **Narudžbe** - kreiranje narudžbi s vremenom preuzimanja
- 👤 **Korisnici** - registracija i prijava
- 🔐 **Admin** - upravljanje jelovnikom i narudžbama

### Uloge:
- **USER** - može pregledavati jelovnik i kreirati narudžbe
- **ADMIN** - može upravljati jelovnikom i svim narudžbama
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Uključi rute
app.include_router(auth_router, prefix="/api/v1")
app.include_router(menu_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Dobrodošli u Menza API!",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
