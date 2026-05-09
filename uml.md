# UML Dijagrami 

## Akteri
- **Korisnik** — prijavljuje se u sustav, pregledava jelovnik, dodaje/briše obroke i kreira narudžbe
- **Administrator** — pregledava sve transakcije i deaktivira korisnike

## Ključni entiteti (klase)
- **Korisnik** — korisnik sustava koji naručuje obroke
- **Admin** — administrator sustava s povišenim ovlastima
- **Obrok** — stavka u jelovniku koja se može naručiti
- **Narudžba** — narudžba koju korisnik kreira, sadrži jedan ili više obroka



## 1. Use Case Dijagram

Korisnik se može prijaviti u sustav, pregledati jelovnik, dodati/obrisati obrok iz narudžbe i kreirati narudžbu. Kreiranje narudžbe uključuje autentikaciju. Dvofaktorska provjera opcionalno proširuje prijavu. Administrator može pregledati sve transakcije i deaktivirati korisnika.

```plantuml

@startuml
left to right direction
actor Korisnik
actor Administrator
rectangle Menza {
  usecase "Prijava u sustav" as UC1
  usecase "Pregled jelovnika" as UC2
  usecase "Dodavanje obroka u košaricu" as UC3
  usecase "Brisanje obroka iz košarice" as UC4
  usecase "Kreiranje narudžbe" as UC5
  usecase "Deaktivacija korisnika" as UC6
  usecase "Pregled svih transakcija" as UC7
  usecase "Autentikacija" as Auth
  usecase "2FA provjera" as TwoFA
}
Korisnik -- UC1
Korisnik -- UC2
Korisnik -- UC3
Korisnik -- UC4
Korisnik -- UC5
Administrator -- UC6
Administrator -- UC7
UC5 ..> Auth : <<include>>
UC1 ..> TwoFA : <<extend>>
@enduml
```

## 2. Sequence Dijagram

### Scenarij 1: Naručivanje obroka

Korisnik šalje zahtjev UI-ju. UI prosljeđuje zahtjev API/serveru. API dohvaća podatke iz baze sustava X-ica. Ako korisnik ima dovoljno sredstava, UI vraća uspješan odgovor s potvrdom i QR kodom; inače prikazuje poruku o pogrešci.

Koraci:
1. Odabir obroka
2. Slanje zahtjeva
3. Provjera stanja sredstava
4. 4.1. Odobreno / 4.2. Odbijeno
5. 5.1. Potvrda narudžbe i QR kod / 5.2. Obavijest o nedostatku sredstava
6. 6.1. Prikaži potvrdu / 6.2. Prikaži pogrešku

```plantuml
@startuml
actor Korisnik
participant "WEB Aplikacija" as UI
participant "Server / API" as API
database "Sustav X-ica" as DB
Korisnik -> UI: Odabir obroka
UI -> API: Slanje zahtjeva za narudžbu
API -> DB: Provjera stanja sredstava
alt Ima dovoljno sredstava
    DB --> API: Odobreno
    API --> UI: Potvrda narudžbe i QR kod
    UI --> Korisnik: Prikaži potvrdu
else Nema dovoljno sredstava
    DB --> API: Odbijeno
    API --> UI: Obavijest o nedostatku sredstava
    UI --> Korisnik: Prikaži pogrešku
end
@enduml
```

### Scenarij 2: Pregledavanje rezervacija

Administrator se prijavljuje u sustav. UI prosljeđuje podatke API-ju. Ako je prijava točna, API dohvaća rezervacije iz baze i vraća ih UI-ju koji ih prikazuje administratoru; inače prikazuje pogrešku.

Koraci:
1. Prijava
2. Provjera podataka
3. Provjera je li prijava ispravna
4. 4.1. Ako je prijava točna — dohvaća rezervacije i vraća ih / 4.2. Ako je netočna — odbij zahtjev
5. Prikaži rezervacije

```plantuml
@startuml
actor Administrator 
participant UI as "Web Aplikacija"
participant API as "Server / API"
database DB as "Baza"
Administrator -> UI : prijava()
activate UI
UI -> API : provjeriPodatke()
activate API
alt tocna prijava
    API -> DB : dohvatiRezervacije()
    activate DB
    DB --> API : rezervacije()
    deactivate DB
    API --> UI : vratiRezervacije
    UI --> Administrator : rezervacije
else netocna prijava 
    API --> UI : odbijZahtjev
    UI --> Administrator : prikaziGresku()
end
deactivate API 
deactivate UI
@enduml
```

---

## 3. Class Dijagram

Sustav se sastoji od četiri klase: Korisnik, Admin, Obrok i Narudžba. Korisnik može kreirati jednu ili više narudžbi. Narudžba sadrži barem jedan obrok. Admin može deaktivirati barem jednog korisnika.

```plantuml
@startuml
left to right direction
class Korisnik{
- ime : String
- prezime : String
- korisnik_id : int
+ naruci_obrok()
+ otkazi_obrok()
}
class Admin{
- admin_id : int
- ime : String
- prezime : String
- razina_ovlasti : String
+ dodaj_obrok()
+ ukloni_obrok()
+ azuriraj_dostupnost()
}
class Obrok {
- obrok_id : int
- naziv : String
- opis : String
- cijena : Decimal
- dostupnost : Boolean
- kolicina : int
}
class Narudžba {
- narudzba_id : int
- korisnik_id : int
- ukupni_iznos : Decimal
- vrijeme_narucivanja : DateTime
}
Korisnik "1" --> "0..*" Narudžba : kreira
Narudžba "1" *-- "1..*" Obrok : sadrži
Admin "1" --> "1..*" Korisnik : deaktivira
@enduml
```
