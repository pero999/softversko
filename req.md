# Projekt: Menza API

## Opis projekta
Sustav narudžbi za menzu/kuhinju - FastAPI REST API s autentikacijom, jelovnikom i narudžbama.
Aplikacija omogućuje korisnicima pregledavanje jelovnika i kreiranje narudžbi,
a administratorima upravljanje jelovnikom (CRUD), postavljanje procijenjenog vremena gotovosti narudžbi i praćenje statusa.

## Članovi tima
- Petar
- Ivona Siric
- Vanessa
- Lorena
- Tomislav Galošević

## GitHub repozitorij
- Link: https://github.com/pero999/softversko
- Svi članovi dodani: DA

---

## User storyji

**US-01** Kao student FESB-a, želim se registrirati u sustav menze sa svojim korisničkim imenom i lozinkom, pregledati dnevni jelovnik s cijenama i kategorijama jela (glavna jela, prilozi, deserti, piće), odabrati željene artikle s količinama, te kreirati narudžbu i dobiti procjenu vremena kada će hrana biti gotova, kako bih znao kada mogu doći u menzu po hranu bez čekanja.

**Scenarij:** Student Marko ima pauzu između predavanja. U 11:30 otvara aplikaciju, pregledava jelovnik, naručuje ćevape s pomfritom i sok. Sustav mu prikazuje potvrdu narudžbe sa statusom "zaprimljena". Administrator menze zaprima narudžbu i postavlja procijenjeno vrijeme gotovosti na 12:15. Marko u aplikaciji vidi da je procijenjeno vrijeme 12:15. U 12:10 dobiva obavijest da je narudžba spremna. Dolazi u menzu, pokazuje broj narudžbe i preuzima hranu.

**US-02** Kao djelatnik menze (administrator), želim se prijaviti u sustav s admin računom, dodavati nove artikle na jelovnik (naziv, cijena, kategorija), ažurirati cijene ili označiti artikle kao nedostupne kada ponestane namirnica, te pratiti sve pristigle narudžbe, postavljati procijenjeno vrijeme gotovosti i mijenjati status narudžbe (zaprimljena → u pripremi → spremna → preuzeta) kako bih mogao organizirati rad kuhinje i informirati studente kada mogu doći po hranu.

**Scenarij:** Djelatnica Ana ujutro dodaje dnevnu ponudu na jelovnik: grah s kobasicom (4.50€), pileći odrezak (5.00€), salata (2.00€). Tijekom dana vidi da je stigla nova narudžba od studenta Marka. Pregledava narudžbu, procjenjuje da će jelo biti gotovo za 45 minuta i postavlja procijenjeno vrijeme na 12:15. Označava narudžbu kao "u pripremi". Kada je narudžba gotova, označava je kao "spremna" - student automatski dobiva obavijest. Kada student preuzme hranu, označava "preuzeto".

---

## Funkcijski zahtjevi

**FZ-01** Sustav mora omogućiti registraciju korisnika putem korisničkog imena i lozinke.
- Prioritet: Visok
- Kriterij prihvaćanja: Korisnik nakon unosa validnog korisničkog imena (min 3 znaka) i lozinke (min 6 znakova) može se prijaviti u sustav.

**FZ-02** Sustav mora omogućiti prijavu korisnika i vraćanje JWT tokena za autentikaciju.
- Prioritet: Visok
- Kriterij prihvaćanja: Korisnik s ispravnim podacima dobiva JWT token; neispravan unos vraća HTTP 401 grešku.

**FZ-03** Sustav mora omogućiti javni pregled jelovnika bez potrebe za prijavom.
- Prioritet: Visok
- Kriterij prihvaćanja: Neprijavljeni korisnik može vidjeti listu svih artikala s nazivom, cijenom i kategorijom.

**FZ-04** Sustav mora omogućiti administratoru dodavanje novog artikla na jelovnik s nazivom, cijenom i kategorijom.
- Prioritet: Visok
- Kriterij prihvaćanja: Samo korisnik s admin ulogom može kreirati artikl; artikl se sprema u bazu i vidljiv je na jelovniku.

**FZ-05** Sustav mora omogućiti administratoru ažuriranje postojećih artikala na jelovniku.
- Prioritet: Visok
- Kriterij prihvaćanja: Admin može promijeniti naziv, cijenu, kategoriju ili dostupnost artikla; promjene su odmah vidljive.

**FZ-06** Sustav mora omogućiti administratoru brisanje artikala s jelovnika.
- Prioritet: Srednji
- Kriterij prihvaćanja: Admin može obrisati artikl; artikl više nije vidljiv na jelovniku.

**FZ-07** Sustav mora omogućiti prijavljenom korisniku kreiranje narudžbe s odabranim artiklima i količinama.
- Prioritet: Visok
- Kriterij prihvaćanja: Narudžba se sprema s listom artikala, količinama, ukupnom cijenom i početnim statusom "pending".

**FZ-08** Sustav mora omogućiti korisniku pregled vlastitih narudžbi, statusa i procijenjenog vremena gotovosti.
- Prioritet: Visok
- Kriterij prihvaćanja: Korisnik vidi samo svoje narudžbe sa statusom (pending, preparing, ready, completed) i procijenjenim vremenom koje je postavio admin.

**FZ-09** Sustav mora omogućiti korisniku otkazivanje vlastite narudžbe koja još nije u pripremi.
- Prioritet: Srednji
- Kriterij prihvaćanja: Korisnik može otkazati narudžbu sa statusom "pending"; narudžbe u pripremi se ne mogu otkazati.

**FZ-10** Sustav mora omogućiti administratoru pregled svih narudžbi, postavljanje procijenjenog vremena gotovosti i promjenu statusa.
- Prioritet: Visok
- Kriterij prihvaćanja: Admin vidi sve narudžbe svih korisnika, može postaviti estimated_time (procijenjeno vrijeme kada će narudžba biti gotova) i promijeniti status iz pending u preparing, ready ili completed.

---

## Nefunkcijski zahtjevi

**NZ-01** Sustav mora vraćati odgovor na API zahtjeve u roku od 500ms za 95% zahtjeva.
- Prioritet: Visok
- Kriterij prihvaćanja: Mjerenjem response time-a u testovima prosječno vrijeme odziva ne prelazi 500ms.

**NZ-02** Sustav mora koristiti JWT autentikaciju s hashiranim lozinkama pomoću bcrypt algoritma.
- Prioritet: Visok
- Kriterij prihvaćanja: Lozinke u bazi nisu čitljive (hashirane); JWT tokeni imaju expiration time od 24 sata.

**NZ-03** Sustav mora imati minimalno 80% pokrivenost koda automatskim testovima.
- Prioritet: Srednji
- Kriterij prihvaćanja: Naredba `pytest --cov` pokazuje code coverage >= 80%.

**NZ-04** Sustav mora biti pokretan putem Docker containera bez dodatne konfiguracije.
- Prioritet: Srednji
- Kriterij prihvaćanja: Naredba `docker compose up --build` uspješno pokreće aplikaciju na portu 8000.

**NZ-05** Sustav mora prolaziti automatske CI/CD provjere (linting, testovi) na svakom git pushu.
- Prioritet: Srednji
- Kriterij prihvaćanja: GitHub Actions workflow prolazi bez grešaka; ruff i pytest ne javljaju probleme.

---

## Taskovi

**TASK-01** Dizajnirati i implementirati SQLModel modele za User, MenuItem, Order i OrderItem
- Povezan sa: FZ-01, FZ-03, FZ-07
- Datoteke: `app/models/user.py`, `app/models/menu_item.py`, `app/models/order.py`

**TASK-02** Implementirati JWT autentikaciju (generiranje tokena, validacija, middleware)
- Povezan sa: FZ-01, FZ-02, NZ-02
- Datoteke: `app/auth.py`

**TASK-03** Implementirati API endpoint za registraciju korisnika
- Povezan sa: FZ-01
- Datoteke: `app/routes/auth.py` - POST `/api/v1/auth/register`

**TASK-04** Implementirati API endpoint za prijavu korisnika
- Povezan sa: FZ-02
- Datoteke: `app/routes/auth.py` - POST `/api/v1/auth/login`

**TASK-05** Implementirati CRUD operacije za jelovnik (dohvat, kreiranje, ažuriranje, brisanje artikala)
- Povezan sa: FZ-03, FZ-04, FZ-05, FZ-06
- Datoteke: `app/routes/menu.py`

**TASK-06** Implementirati kreiranje narudžbi s validacijom artikala i izračunom cijene
- Povezan sa: FZ-07
- Datoteke: `app/routes/orders.py` - POST `/api/v1/orders/`

**TASK-07** Implementirati pregled i otkazivanje vlastitih narudžbi za korisnike
- Povezan sa: FZ-08, FZ-09
- Datoteke: `app/routes/orders.py` - GET `/api/v1/orders/my`, DELETE `/api/v1/orders/my/{id}`

**TASK-08** Implementirati admin funkcionalnosti za pregled narudžbi, postavljanje procijenjenog vremena i promjenu statusa
- Povezan sa: FZ-10
- Datoteke: `app/routes/orders.py` - GET `/api/v1/orders/`, PATCH `/api/v1/orders/{id}/status`, PATCH `/api/v1/orders/{id}/estimated-time`

**TASK-09** Napisati unit testove za autentikaciju, modele i validacije
- Povezan sa: NZ-03
- Datoteke: `tests/test_unit.py`

**TASK-10** Napisati integracijske testove za kompletne korisničke tokove
- Povezan sa: NZ-03
- Datoteke: `tests/test_integration.py`

**TASK-11** Kreirati Dockerfile i docker-compose.yml za kontejnerizaciju
- Povezan sa: NZ-04
- Datoteke: `Dockerfile`, `docker-compose.yml`

**TASK-12** Postaviti GitHub Actions CI/CD workflow s lintingom i testovima
- Povezan sa: NZ-05
- Datoteke: `.github/workflows/ci.yml`

**TASK-13** Implementirati seed skriptu za demo podatke (admin, korisnici, artikli)
- Povezan sa: svi zahtjevi
- Datoteke: `app/seed.py`

**TASK-14** Napisati README dokumentaciju s uputama za pokretanje
- Povezan sa: svi zahtjevi
- Datoteke: `README.md`

---

## Raspodjela zadataka

| Član tima          | Funkcijski zahtjevi | Nefunkcijski zahtjevi | Taskovi                    |
|--------------------|---------------------|----------------------|----------------------------|
| Petar              | FZ-01, FZ-02        | NZ-02                | TASK-02, TASK-03, TASK-04  |
| Ivona Siric        | FZ-03, FZ-04        | NZ-03                | TASK-05, TASK-09           |
| Vanessa            | FZ-05, FZ-06        | NZ-04                | TASK-01, TASK-11           |
| Lorena             | FZ-07, FZ-08        | NZ-05                | TASK-06, TASK-07, TASK-12  |
| Tomislav Galošević | FZ-09, FZ-10        | NZ-01                | TASK-08, TASK-10, TASK-13, TASK-14 |

---

## Tehnološki stack

| Kategorija | Tehnologija |
|------------|-------------|
| Jezik | Python 3.11+ |
| Web Framework | FastAPI |
| ASGI Server | Uvicorn |
| Baza podataka | SQLite |
| ORM | SQLModel |
| Autentikacija | JWT (python-jose) |
| Hashiranje lozinki | bcrypt (passlib) |
| Testiranje | pytest |
| Linting | ruff, black |
| CI/CD | GitHub Actions |
| Kontejnerizacija | Docker |

---

## API Endpoints

### Autentikacija (`/api/v1/auth`)
| Metoda | Endpoint    | Opis                        | Auth    |
|--------|-------------|-----------------------------|---------|
| POST   | `/register` | Registracija novog korisnika | -       |
| POST   | `/login`    | Prijava (vraća JWT token)   | -       |
| GET    | `/me`       | Dohvati podatke o prijavljenom korisniku | JWT |

### Jelovnik (`/api/v1/menu`)
| Metoda | Endpoint | Opis              | Auth   |
|--------|----------|-------------------|--------|
| GET    | `/`      | Dohvati cijeli jelovnik | Javno  |
| GET    | `/{id}`  | Dohvati pojedini artikl | Javno  |
| POST   | `/`      | Dodaj novi artikl | Admin  |
| PATCH  | `/{id}`  | Ažuriraj artikl   | Admin  |
| DELETE | `/{id}`  | Obriši artikl     | Admin  |

### Narudžbe (`/api/v1/orders`)
| Metoda | Endpoint              | Opis                              | Auth  |
|--------|-----------------------|-----------------------------------|-------|
| POST   | `/`                   | Kreiraj novu narudžbu             | User  |
| GET    | `/my`                 | Dohvati moje narudžbe             | User  |
| GET    | `/my/{id}`            | Dohvati moju narudžbu             | User  |
| DELETE | `/my/{id}`            | Otkaži moju narudžbu              | User  |
| GET    | `/`                   | Dohvati sve narudžbe              | Admin |
| GET    | `/{id}`               | Dohvati narudžbu po ID            | Admin |
| PATCH  | `/{id}/status`        | Promijeni status narudžbe         | Admin |
| PATCH  | `/{id}/estimated-time`| Postavi procijenjeno vrijeme gotovosti | Admin |
