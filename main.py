"""Glavna FastAPI aplikacija - Sustav narudžbi za menzu."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import select

from app.config import get_settings
from app.database import create_db_and_tables, get_session
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.menu import router as menu_router
from app.routes.orders import router as orders_router
from app.seed import seed_database

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle eventi aplikacije."""
    # Startup: kreiraj tablice
    create_db_and_tables()

    # Auto-seed ako je baza prazna
    session = next(get_session())
    try:
        existing_user = session.exec(select(User)).first()
        if existing_user is None:
            print("Baza je prazna - pokrecem seed...")
            seed_database()
            print("Seed zavrsen!")
    finally:
        session.close()

    yield
    # Shutdown: cleanup ako treba


# CORS - dozvoli frontend pristup
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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uključi API rute
app.include_router(auth_router, prefix="/api/v1")
app.include_router(menu_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")

# Frontend static files
FRONTEND_DIR = Path(__file__).parent / "frontend"


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api")
def api_info():
    """API info endpoint."""
    return {
        "message": "Menza API",
        "docs": "/docs",
        "version": "1.0.0",
    }


# Serve frontend static files (CSS, JS)
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend():
        """Serve frontend index.html."""
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/admin.html")
    def serve_admin():
        """Serve admin panel."""
        return FileResponse(FRONTEND_DIR / "admin.html")

    @app.get("/styles.css")
    def serve_css():
        """Serve CSS."""
        return FileResponse(FRONTEND_DIR / "styles.css")

    @app.get("/app.js")
    def serve_js():
        """Serve JavaScript."""
        return FileResponse(FRONTEND_DIR / "app.js")
