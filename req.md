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
US-01 Kao student, želim pregledati jelovnik i biti u mogućnosti rezervirati jelo za sljedeći dan.
US-02 Kao administrator, želim pregledati sve
rezervacije jela kako bih mogao znati koliko jela trebam pripremiti za naredni dan.

## Funkcijski zahtjevi
FZ-01 Sustav mora prikazati cijeli jelovnik.
FZ-02 Sustav mora omogućiti rezervaciju slobodnog
jela za naredni dan.
FZ-03 Sustav mora spriječiti rezervaciju jela ako više nema dostupne količine.
FZ-04 Sustav mora omogućiti otkazivanje narudžbe.
FZ-05 Sustav mora omogućiti brisanje pogrešno odabranog obroka prije potvrđivanja.
FZ-06 Sustav mora omogućiti uređivanje obroka prema želji.
FZ-07 Korisnik može promjeniti temu straice.
FZ-08 Sustav mora omogućiti prikaz prošlih naredbi.
...

## Nefunkcijski zahtjevi
NZ-01 Sustav mora vratiti popis jela u roku od 4
sekunde za 95% zahtjeva.
NZ-02 Sustav mora bilježiti greške pri neuspjeloj
rezervaciji(npr ako je prijeđena dostupna količina).
NZ-03 Sustav mora u roku od 2 sekunde promjeniti temu stranice na zahtjev.
NZ-04 Sustav je dostupan 99% vremena. 
...

## Taskovi
TASK-01 Napraviti model baze za termin i rezervaciju.
TASK-02 Implementirati API za dohvat slobodnih obroka.
TASK-03 Implementirati validaciju zauzetog obroka.
TASK-04 Napisati test rezervacije.

## Raspodjela zadataka
Ivona: FZ-01, FZ-02, NZ-01, TASK-01
Vanessa: FZ-04, NZ-02, TASK-03
Lorena: FZ-05, FZ-06, NZ-03
Petar: FZ-08, TASK-02
Tomislav: TASK-04, FZ-03
