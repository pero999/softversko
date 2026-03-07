"""Seed skripta za demo podatke."""

from decimal import Decimal

from sqlmodel import Session, select

from app.auth import get_password_hash
from app.database import create_db_and_tables, engine
from app.models.menu_item import MenuItem
from app.models.user import User, UserRole


def seed_database():
    """Popuni bazu s demo podacima."""
    create_db_and_tables()

    with Session(engine) as session:
        # Provjeri da li već postoje podaci
        existing_users = session.exec(select(User)).first()
        if existing_users:
            print("Baza već ima podatke. Preskačem seeding.")
            return

        print("Kreiram demo korisnike...")

        # Kreiraj admin korisnika
        admin = User(
            username="admin",
            email="admin@menza.hr",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin)

        # Kreiraj običnog korisnika
        user = User(
            username="korisnik",
            email="korisnik@menza.hr",
            full_name="Demo Korisnik",
            hashed_password=get_password_hash("korisnik123"),
            role=UserRole.USER,
            is_active=True,
        )
        session.add(user)

        # Kreiraj još jednog korisnika
        user2 = User(
            username="marko",
            email="marko@student.hr",
            full_name="Marko Marković",
            hashed_password=get_password_hash("marko123"),
            role=UserRole.USER,
            is_active=True,
        )
        session.add(user2)

        print("Kreiram jelovnik...")

        # Kreiraj artikle jelovnika
        menu_items = [
            # Glavna jela
            MenuItem(
                name="Pileći odrezak s rižom",
                description="Pileći odrezak na žaru s prilogom riže i sezonskim povrćem",
                price=Decimal("7.50"),
                category="Glavna jela",
                is_available=True,
            ),
            MenuItem(
                name="Ćevapi s lukom",
                description="10 ćevapa s lukom, kajmakom i somun kruhom",
                price=Decimal("8.00"),
                category="Glavna jela",
                is_available=True,
            ),
            MenuItem(
                name="Vegetarijanska lazanja",
                description="Lazanja s povrćem i sirom",
                price=Decimal("6.50"),
                category="Glavna jela",
                is_available=True,
            ),
            MenuItem(
                name="Pohani šnicl s krumpirom",
                description="Svinjski pohani šnicl s pire krumpirom",
                price=Decimal("7.00"),
                category="Glavna jela",
                is_available=False,  # Nedostupno
            ),
            # Juhe
            MenuItem(
                name="Goveđa juha s rezancima",
                description="Domaća goveđa juha",
                price=Decimal("2.50"),
                category="Juhe",
                is_available=True,
            ),
            MenuItem(
                name="Krem juha od brokule",
                description="Krem juha od svježe brokule",
                price=Decimal("2.50"),
                category="Juhe",
                is_available=True,
            ),
            # Salate
            MenuItem(
                name="Miješana salata",
                description="Zelena salata, rajčica, krastavac",
                price=Decimal("2.00"),
                category="Salate",
                is_available=True,
            ),
            MenuItem(
                name="Cezar salata",
                description="Cezar salata s piletinom i krutonima",
                price=Decimal("5.50"),
                category="Salate",
                is_available=True,
            ),
            # Deserti
            MenuItem(
                name="Palačinke s Nutellom",
                description="2 palačinke s Nutellom i šlagom",
                price=Decimal("3.50"),
                category="Deserti",
                is_available=True,
            ),
            MenuItem(
                name="Voćna salata",
                description="Sezonsko voće",
                price=Decimal("3.00"),
                category="Deserti",
                is_available=True,
            ),
            # Piće
            MenuItem(
                name="Coca-Cola 0.5L",
                description="",
                price=Decimal("2.00"),
                category="Piće",
                is_available=True,
            ),
            MenuItem(
                name="Voda 0.5L",
                description="",
                price=Decimal("1.00"),
                category="Piće",
                is_available=True,
            ),
        ]

        for item in menu_items:
            session.add(item)

        session.commit()
        print("✅ Demo podaci uspješno kreirani!")
        print()
        print("Demo korisnici:")
        print("  👤 Admin:    admin / admin123")
        print("  👤 Korisnik: korisnik / korisnik123")
        print("  👤 Korisnik: marko / marko123")


if __name__ == "__main__":
    seed_database()
