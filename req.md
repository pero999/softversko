# Projekt: Rezervacija termina
## Članovi tima
- Ivona Širić
- Vanessa Vinković
- Lorena Ištvanović
- Tomislav Galošević
- Petar Pavan
  
## GitHub repozitorij
- Link: https://github.com/pero999/softversko/new/main
- Svi članovi dodani: DA
  
## User storyji
US-01 Kao korisnik, želim pregledati jelovnik i biti u mogućnosti rezervirati jelo za sljedeći dan.
US-02 Kao administrator, želim pregledati sve
rezervacije jela kako bih mogao znati koliko jela trebam pripremiti za naredni dan.
US-03 Kao korisnik, želim primiti potvrdu rezervacije nakon narudžbe kako bih bio siguran da je moja rezervacija uspješno zaprimljena.

## Funkcijski zahtjevi
FZ-01 Sustav mora prikazati cijeli jelovnik.
FZ-02 Sustav mora omogućiti rezervaciju slobodnog jela za naredni dan.
FZ-03 Sustav mora spriječiti rezervaciju jela ako više nema dostupne količine.
FZ-04 Sustav mora omogućiti otkazivanje narudžbe.
FZ-05 Sustav mora omogućiti brisanje pogrešno odabranog obroka prije potvrđivanja.
FZ-06 Sustav mora omogućiti uređivanje obroka prema želji.
FZ-07 Korisnik može promjeniti temu stranice.
FZ-08 Sustav mora omogućiti prikaz prošlih naredbi.
FZ-09 Sustav mora omogućiti korisniku registraciju korisničkog računa.
FZ-10 Sustav mora omogućiti administratoru pregled ukupnog broja rezervacija po jelu za odabrani datum.

## Nefunkcijski zahtjevi
NZ-01 Sustav mora vratiti popis jela u roku od 4 sekunde za 95% zahtjeva.
NZ-02 Sustav mora bilježiti greške pri neuspjeloj rezervaciji(npr ako je prijeđena dostupna količina).
NZ-03 Sustav mora u roku od 2 sekunde promjeniti temu stranice na zahtjev.
NZ-04 Sustav mora omogućiti rezervaciju obroka u manje od 6 koraka. 
NZ-05 Sustav napravljen u obliku mikroservisa i containeri
NZ-06 Sustav mora proći 95% testova prije odlaska u produkciju


## Taskovi
TASK-01 Dizajnirati i napraviti SQL modele za korisnika, jelovnik i narudzbu.
TASK-02 Implementirati API za registraciju i prijavu korisnika.
TASK-03 Implementirati kreiranje narudžbi s validacijom artikla i izračunom cijene.
TASK-04 Implementirati pregled i otkazivanje vlastitih narudžbi za korisnike
TASK-05 Napisati unit testove za autentifikaciju, modele i validacije.
TASK-06 testirati kreiranje narudžbe, dohvat vlastitih narudžbi, otkazivanje narudžbe.
TASK-07 Testirati slučaj krive zaporke pri prijavi te nepostojećeg korisnika.
TASK-08 Implementirati registraciju korisničkog računa.
TASK-09 Implementirati administratorski pregled broja rezervacija po jelu za odabrani datum.


## Raspodjela zadataka
Ivona: FZ-01, FZ-02, NZ-01, TASK-01, TASK-08
Vanessa: FZ-04, FZ-09, NZ-02, TASK-03, TASK-09
Lorena: FZ-05, FZ-06, NZ-03, NZ-06, TASK-02
Petar: FZ-08, FZ-07, NZ-04, TASK-04, TASK-07
Tomislav: FZ-03, FZ-10, NZ-05, TASK-05, TASK-06
