# UML modeli sustava (Menza API)

Ovaj dokument sadrži tri tražena UML dijagrama za projekt `Menza API`:
- Use Case dijagram
- Sequence dijagram (scenarij: korisnik kreira narudžbu)
- Class dijagram

## 1) Use Case dijagram

**Kratko objašnjenje**

Sustav koriste dva glavna aktera: `Korisnik` i `Administrator`.
Korisnik se registrira/prijavljuje, pregledava jelovnik i kreira vlastite narudžbe.
Administrator, uz prijavu, upravlja jelovnikom i statusima narudžbi.
Za zaštićene funkcionalnosti autentikacija je obavezna (`<<include>>`), dok je otkazivanje narudžbe opcionalno proširenje toka rada narudžbe (`<<extend>>`).

**PlantUML kod**

```plantuml
@startuml
left to right direction

actor "Korisnik" as User
actor "Administrator" as Admin

rectangle "Menza API Sustav" {
  usecase "Registracija" as UC_Register
  usecase "Prijava" as UC_Login
  usecase "Autentikacija" as UC_Auth
  usecase "Pregled jelovnika" as UC_ViewMenu
  usecase "Kreiranje narudžbe" as UC_CreateOrder
  usecase "Pregled mojih narudžbi" as UC_MyOrders
  usecase "Otkazivanje narudžbe" as UC_CancelOrder
  usecase "Upravljanje jelovnikom\n(CRUD)" as UC_MenuCRUD
  usecase "Pregled svih narudžbi" as UC_AllOrders
  usecase "Promjena statusa narudžbe" as UC_UpdateStatus
}

User -- UC_Register
User -- UC_Login
User -- UC_ViewMenu
User -- UC_CreateOrder
User -- UC_MyOrders
User -- UC_CancelOrder

Admin -- UC_Login
Admin -- UC_MenuCRUD
Admin -- UC_AllOrders
Admin -- UC_UpdateStatus

UC_CreateOrder ..> UC_Auth : <<include>>
UC_MyOrders ..> UC_Auth : <<include>>
UC_MenuCRUD ..> UC_Auth : <<include>>
UC_AllOrders ..> UC_Auth : <<include>>
UC_UpdateStatus ..> UC_Auth : <<include>>
UC_CancelOrder ..> UC_CreateOrder : <<extend>>
@enduml
```

## 2) Sequence dijagram

**Kratko objašnjenje**

Scenarij prikazuje tok kreiranja narudžbe:
1) korisnik šalje zahtjev API-ju,
2) API validira vrijeme preuzimanja i stavke,
3) API provjerava svaki artikl u bazi,
4) ako je sve valjano, kreira narudžbu i stavke, te vraća uspješan odgovor.
U slučaju greške koristi se `alt` grana (npr. nepostojeći/nedostupan artikl ili vrijeme u prošlosti).

**PlantUML kod**

```plantuml
@startuml
actor Korisnik
participant "API /orders" as API
participant "Auth (JWT)" as Auth
database "SQLite baza" as DB

Korisnik -> API : POST /api/v1/orders (pickup_time, items)
API -> Auth : validiraj token
Auth --> API : korisnik autoriziran

API -> API : validiraj pickup_time > now
alt neispravno vrijeme
  API --> Korisnik : 400 Bad Request
else vrijeme je valjano
  loop za svaku stavku narudžbe
    API -> DB : dohvati MenuItem(menu_item_id)
    alt artikl ne postoji ili nije dostupan
      API --> Korisnik : 404/400 greška
    else artikl valjan
      API -> API : izračunaj item_total i total_price
    end
  end

  API -> DB : insert Order(status=pending, total_price)
  API -> DB : insert OrderItem(...)
  DB --> API : spremljeno
  API --> Korisnik : 201 Created + OrderRead
end
@enduml
```

## 3) Class dijagram

**Kratko objašnjenje**

Domena se sastoji od korisnika, artikala jelovnika, narudžbi i stavki narudžbe.
Jedan korisnik može imati više narudžbi, a jedna narudžba sadrži jednu ili više stavki.
Svaka stavka se odnosi na jedan artikl jelovnika i pamti količinu i cijenu po jedinici u trenutku narudžbe.
Ulogu korisnika (`user/admin`) modelira enum `UserRole`, a stanje narudžbe enum `OrderStatus`.

**PlantUML kod**

```plantuml
@startuml

enum UserRole {
  user
  admin
}

enum OrderStatus {
  pending
  confirmed
  ready
  completed
  cancelled
}

class User {
  +id: int
  +username: str
  +email: str
  +full_name: str?
  +hashed_password: str
  +is_active: bool
  +role: UserRole
  +created_at: datetime
  +updated_at: datetime
}

class MenuItem {
  +id: int
  +name: str
  +description: str?
  +price: Decimal
  +is_available: bool
  +category: str?
  +created_at: datetime
  +updated_at: datetime
}

class Order {
  +id: int
  +user_id: int
  +pickup_time: datetime
  +note: str?
  +status: OrderStatus
  +total_price: Decimal
  +created_at: datetime
  +updated_at: datetime
}

class OrderItem {
  +id: int
  +order_id: int
  +menu_item_id: int
  +quantity: int
  +unit_price: Decimal
}

User "1" --> "0..*" Order : kreira
Order "1" *-- "1..*" OrderItem : sadrži
MenuItem "1" --> "0..*" OrderItem : je_stavka_u
User --> UserRole
Order --> OrderStatus

@enduml
```
