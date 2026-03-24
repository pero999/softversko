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

CLASS DIJAGRAM
Klase korisnik, admin, obrok i narudžba
Atribut: korisnik: ime, prezime, korisnik_id
         admin: admin_id, ime, prezime, razina_ovlasti
         obrok: obrok_id, naziv, opis, cijena, dostupnost
         narudžba: narudžba_id, korisnik_id, ukupni_iznos, vrijeme_narucivanja
Jedna narudžba 


