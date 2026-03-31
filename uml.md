USE CASE DIJAGRAM
Korisnik se može prijaviti u sustav, pregledati jelovnik, dodati/obristai obrok iz narudžbe
i kreirati narudžbu. Kreiranje narudžbe uključuje autentikaciju. Dvofaktorska provjera opcionalno proširuje prijavu.
Administartor može pregledati sve transkacije i deaktivirati korisnika

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
  usecase "Pregled svih korisnika" as UC7
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
TwoFA ..> UC1 : <<extend>>
@enduml

}

SEQUENCE DIJAGRAM
Scenarij: naručivanje obroka
1. odabir obroka 2. slanje zahtjeva 3. provjera stanja sredstava
4.1. odobreno 4.2. odbijeno 5.1 potvrda narudžbe i QR kod 5.2. obavijest o nedostatku sredstava 6.1. prikaži potvrdu 6.2. prikaži pogrešku
Korisnik šalje zahtjev UI-ju. UI prosljeđuje zahtjev API/serveru. API dohvaća podatke iz
baze sustava X-ica. Ako korisnik ima dovoljno sredstava UI vraća uspješan odgovor; inače poruku o pogrešci.

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

Scenarij: pregledavanje rezervacija 
1. Prijava 2. Provjerava podatke 3. Dohvaća rezervacije 4. Provjerava je li prijava ispravna 4.1 Ako je prijava točna vrati rezervacije 4.2 Ako je netočna odbij zahtjev 5. Prikaži rezervacije

@startuml
actor Administrator 
participant UI as "Web Aplikacija"
participant API as "Server / API"
database DB as "Baza"

Administrator -> UI : prijava()
activate UI
UI -> API : provjeriPodatke()
activate API
API -> DB : dohvatiRezervacije()
activate DB
DB --> API : rezervacije()
deactivate DB

alt tocna prijava
API --> UI : vratiRezervacije
else netocna prijava 
API --> UI : odbijZahtjev
end

UI --> Administrator : rezervacije
deactivate API 
deactivate UI
@enduml

CLASS DIJAGRAM
Klase korisnik, admin, obrok i narudžba
Atribut: korisnik: ime, prezime, korisnik_id
         admin: admin_id, ime, prezime, razina_ovlasti
         obrok: obrok_id, naziv, opis, cijena, dostupnost, kolicina
         narudžba: narudžba_id, korisnik_id, ukupni_iznos, vrijeme_narucivanja
Admin može deaktivirati barem jednog korisnika. Korisnik može napraviti jednu ili više narudžbi. Narudžba sadrži barem jedan obrok. Obrok može ili ne mora biti stavka u narudžbi. 
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
- dostupnost : Bull
- kolicina : int
}

class Narudžba {
- narudba_id : int
- korisnik_id : int
- ukupni_iznos : Decimal
- vrijeme_narucivanja : DateTime
}

Korisnik "1" --> "0..*" Narudžba : kreira
Narudžba "1" *-- "1..*" Obrok : sadrži
Obrok "1" --> "0..*" Narudžba : je_stavka_u
Admin "1" --> "1..*" Korisnik : deaktivira


