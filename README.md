# Softversko API

FastAPI REST API projekt s SQLModel i SQLite bazom podataka.

## 🚀 Brzi start

### Lokalno pokretanje

```bash
# Instaliraj dependencije
pip install -r requirements.txt

# Pokreni server
uvicorn main:app --reload

# Otvori dokumentaciju
# http://localhost:8000/docs
```

### Docker pokretanje

```bash
# Build i pokreni
docker-compose up --build

# Ili za development s auto-reload
docker-compose --profile dev up --build
```

## 📁 Struktura projekta

```
softversko/
├── app/
│   ├── models/          # SQLModel database modeli
│   ├── routes/          # API rute (endpoints)
│   ├── schemas/         # Pydantic sheme
│   ├── config.py        # Konfiguracija
│   └── database.py      # Database setup
├── tests/               # Pytest testovi
├── data/                # SQLite baza (gitignored)
├── .github/workflows/   # GitHub Actions CI
├── main.py              # FastAPI aplikacija
├── requirements.txt     # Python dependencije
├── Dockerfile           # Docker image
└── docker-compose.yml   # Docker Compose
```

## 🔧 Razvoj

### Testiranje

```bash
pytest -v
```

### Linting i formatiranje

```bash
# Provjeri lint greške
ruff check .

# Automatski popravi
ruff check --fix .

# Formatiraj kod
black .
```

## 📚 API Dokumentacija

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔗 API Endpoints

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/api/v1/users/` | Dohvati sve usere |
| POST | `/api/v1/users/` | Kreiraj usera |
| GET | `/api/v1/users/{id}` | Dohvati usera |
| PATCH | `/api/v1/users/{id}` | Ažuriraj usera |
| DELETE | `/api/v1/users/{id}` | Obriši usera |

## 👥 Tim

- Petar
- Ivona Siric
- Vanessa
- Lorena
