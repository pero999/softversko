"""Database konfiguracija i session management."""

from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

settings = get_settings()

# Kreiraj engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False},  # Potrebno za SQLite
)


def create_db_and_tables():
    """Kreiraj bazu i tablice."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency za dohvat database sessiona."""
    with Session(engine) as session:
        yield session
