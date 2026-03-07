# 🍽️ Menza API

Sustav narudžbi za menzu/kuhinju - FastAPI REST API s autentikacijom, jelovnikom i narudžbama.

## 📋 Opis projekta

Aplikacija omogućuje:
- **Korisnicima**: pregledavanje jelovnika i kreiranje narudžbi s vremenom preuzimanja
- **Administratorima**: upravljanje jelovnikom (CRUD) i pregled svih narudžbi

## 🛠️ Tehnološki stack

| Kategorija | Tehnologija |
|------------|-------------|
| Jezik | Python 3.11+ |
| Web Framework | FastAPI |
| ASGI Server | Uvicorn |
| Baza podataka | SQLite |
| ORM | SQLModel |
| Autentikacija | JWT (python-jose) |
| Testiranje | pytest |
| Linting | ruff, black |
| CI/CD | GitHub Actions |
| Kontejnerizacija | Docker |

## 🚀 Brzi start

### Preduvjeti

- Python 3.11+
- pip
- Git
- Docker (opcionalno)

### Lokalno pokretanje

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/pero999/softversko.git
cd softversko

# 2. Instaliraj dependencije
pip install -r requirements.txt

# 3. Pokreni seed skriptu za demo podatke
python -m app.seed

# 4. Pokreni server
uvicorn main:app --reload

# 5. Otvori dokumentaciju
# http://localhost:8000/docs
```

### Docker pokretanje

```bash
# Build i pokreni
docker compose up --build
```

## 👥 Demo korisnici

| Uloga | Username | Lozinka |
|-------|----------|---------|
| 👑 Admin | `admin` | `admin123` |
| 👤 Korisnik | `korisnik` | `korisnik123` |
| 👤 Korisnik | `marko` | `marko123` |

## 📚 API Dokumentacija

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 API Endpoints

### Autentikacija (`/api/v1/auth`)

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| POST | `/register` | Registracija korisnika | ❌ |
| POST | `/login` | Prijava (vraća JWT) | ❌ |
| GET | `/me` | Dohvati trenutnog korisnika | ✅ |

### Jelovnik (`/api/v1/menu`)

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| GET | `/` | Dohvati jelovnik | ❌ Javno |
| GET | `/{id}` | Dohvati artikl | ❌ Javno |
| POST | `/` | Kreiraj artikl | 👑 Admin |
| PATCH | `/{id}` | Ažuriraj artikl | 👑 Admin |
| DELETE | `/{id}` | Obriši artikl | 👑 Admin |

### Narudžbe (`/api/v1/orders`)

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| POST | `/` | Kreiraj narudžbu | ✅ User |
| GET | `/my` | Moje narudžbe | ✅ User |
| GET | `/my/{id}` | Moja narudžba | ✅ User |
| DELETE | `/my/{id}` | Otkaži narudžbu | ✅ User |
| GET | `/` | Sve narudžbe | 👑 Admin |
| GET | `/{id}` | Narudžba po ID | 👑 Admin |
| PATCH | `/{id}/status` | Promijeni status | 👑 Admin |

## 🎬 Demo scenarij

### 1. Prijava kao admin
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=admin&password=admin123"
```

### 2. Dodaj novi artikl na jelovnik
```bash
curl -X POST "http://localhost:8000/api/v1/menu/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Burek", "price": "2.50", "category": "Pekara"}'
```

### 3. Prijava kao korisnik i kreiranje narudžbe
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=korisnik&password=korisnik123"

# Kreiraj narudžbu
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_time": "2024-12-20T12:00:00Z",
    "items": [{"menu_item_id": 1, "quantity": 2}]
  }'
```

## 🧪 Testiranje

```bash
# Pokreni sve testove
pytest -v

# Pokreni s coverage izvještajem
pytest --cov=app --cov-report=html
```

### Testovi:
- **Unit testovi** (15+): auth, modeli, validacije
- **Integracijski testovi** (4): kompletni tokovi

## 🔍 Linting i formatiranje

```bash
# Provjeri lint greške
ruff check .

# Automatski popravi
ruff check --fix .

# Formatiraj kod
black .
```

## 📁 Struktura projekta

```
softversko/
├── .github/workflows/     # GitHub Actions CI
│   └── ci.yml
├── app/
│   ├── models/            # SQLModel modeli
│   │   ├── user.py        # User + uloge
│   │   ├── menu_item.py   # MenuItem (artikli)
│   │   └── order.py       # Order + OrderItem
│   ├── routes/            # API rute
│   │   ├── auth.py        # Registracija, login
│   │   ├── menu.py        # CRUD jelovnika
│   │   └── orders.py      # Narudžbe
│   ├── auth.py            # JWT autentikacija
│   ├── config.py          # Postavke
│   ├── database.py        # Database setup
│   └── seed.py            # Demo podaci
├── tests/                 # Pytest testovi
│   ├── conftest.py        # Fixtures
│   ├── test_unit.py       # Unit testovi
│   ├── test_integration.py # Integracijski
│   └── test_main.py       # API testovi
├── data/                  # SQLite baza
├── main.py                # FastAPI app
├── requirements.txt       # Dependencije
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## ✅ MVP Checklist

- [x] Dvije uloge (User + Admin)
- [x] JWT autentikacija
- [x] Javni jelovnik (MenuItem CRUD)
- [x] Narudžbe s vremenom preuzimanja
- [x] Validacija nedostupnih artikala
- [x] 15+ unit testova
- [x] 4+ integracijska testa
- [x] GitHub Actions CI
- [x] Docker podrška
- [x] Seed skripta za demo

## 👥 Tim

- Petar
- Ivona Siric
- Vanessa
- Lorena

## 📄 Licenca

MIT
