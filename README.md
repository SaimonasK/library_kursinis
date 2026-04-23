# library_kursinis

# Library

**Objektinio programavimo kursinis darbas**  
**Studentas:** Saimonas Kuckailis  
**Grupė:** EDIf-25/1  

---

## Turinys

1. [Įvadas](#įvadas)
2. [Analizė](#analizė)
3. [Rezultatai ir išvados](#rezultatai-ir-išvados)
4. [Šaltiniai](#šaltiniai)

---

## Įvadas

### Kas tai per programa?

Library — tai komandinės eilutės (CLI) programa, skirta valdyti bibliotekos knygų, žurnalų, narių ir skolinimų įrašus. Sistema leidžia:

- Pridėti ir šalinti bibliotekos objektus (knygas, žurnalus)
- Registruoti bibliotekos narius
- Fiksuoti skolinimą ir grąžinimą
- Ieškoti objektų pagal pavadinimą
- Išsaugoti ir užkrauti duomenis iš CSV failų

### Kaip paleisti programą?

1. Atsisiųsti visus projekto failus ir sudėti tokia struktūra:

```
library_kursinis/
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── items.py
│   └── people.py
├── library.py
├── cli.py
├── main.py
└── tests.py
```

2. Terminale pereiti į projekto aplanką:

```bash
cd library_kursinis
```

3. Paleisti interaktyvią programą:

```bash
python cli.py
```

4. Paleisti unit testus:

```bash
python -m unittest tests -v
```

### Kaip naudotis programa?

Paleidus `cli.py`, ekrane pasirodo meniu:

```
=== Vilnius Tech biblioteka ===
Items: 0 | Members: 0 | Active loans: 0
1. List available items
2. Search items
3. Add book
4. Add magazine
5. Register member
6. List members
7. Borrow item
8. Return item
9. List active loans
s. Save to CSV
q. Quit
```

Naudotojas įveda skaičių arba raidę ir paspaudžia Enter. Programa paprašo reikiamos informacijos žingsnis po žingsnio. Duomenys automatiškai išsaugomi į `data/` aplanką po kiekvieno veiksmo.

---

## Analizė

### 1. OOP 4 principai

#### Abstrakcija (*Abstraction*)

Abstrakcija — tai principas, kuris slepia detales ir parodo tik esminę sąsają. Šiame projekte abstrakcija įgyvendinta per abstrakčias bazines klases `LibraryItem` ir `Person`, naudojant Python `abc` modulį.

```python
from abc import ABC, abstractmethod

class LibraryItem(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass
```

`LibraryItem` klasės negalima tiesiogiai sukurti — ji tik apibrėžia, ką privalo turėti kiekvienas bibliotekos objektas. Tai užtikrina, kad visos subklasės (`Book`, `Magazine`) turės `get_info()` metodą.

---

#### Inkapsuliacija (*Encapsulation*)

Inkapsuliacija — tai duomenų ir metodų apjungimas į klasę bei prieigos prie duomenų apribojimas. Šiame projekte visi atributai yra privatūs (su `__` prefiksu) ir pasiekiami tik per `@property`:

```python
class LibraryItem(ABC):
    def __init__(self, item_id: str, title: str, year: int):
        self.__item_id = item_id
        self.__title = title
        self.__is_available = True

    @property
    def title(self) -> str:
        return self.__title      

    @is_available.setter
    def is_available(self, value: bool):
        self.__is_available = value
```

Tai apsaugo duomenis nuo tiesioginio keitimo iš išorės.

---

#### Paveldėjimas (*Inheritance*)

Paveldėjimas leidžia klasei perimti kitos klasės atributus ir metodus. `Book` ir `Magazine` paveldi iš `LibraryItem`, o `Member` ir `Librarian` — iš `Person`:

```python
class Book(LibraryItem):
    def __init__(self, item_id, title, year, author, isbn, genre):
        super().__init__(item_id, title, year)
        self.__author = author
        self.__isbn = isbn
        self.__genre = genre
```

Dėl paveldėjimo `Book` klasė automatiškai gauna `item_id`, `title`, `year`, `is_available` atributus ir nereikia jų rašyti iš naujo.

---

#### Polimorfizmas (*Polymorphism*)

Polimorfizmas leidžia skirtingoms klasėms turėti tą patį metodo pavadinimą, bet skirtingą elgesį. `get_info()` metodas veikia skirtingai `Book` ir `Magazine` klasėse:

```python
class Book(LibraryItem):
    def get_info(self) -> str:
        return (
            f"Book | {self.title}\n"
            f"  Author : {self.__author}\n"
            f"  ISBN   : {self.__isbn}\n"
        )

class Magazine(LibraryItem):
    def get_info(self) -> str:
        return (
            f"Magazine | {self.title}\n"
            f"  Issue  : #{self.__issue_number}\n"
            f"  Publisher : {self.__publisher}\n"
        )
```

Programoje galima iteruoti per visus objektus ir kviesti `get_info()` nežinant tikslaus tipo:

```python
for item in lib.list_available_items():
    print(item.get_info()) 
```

---

### 2. Dizaino šablonas — Singleton

**Singleton** šablonas užtikrina, kad klasės objektas bus sukurtas tik vieną kartą. Tai tinkamas pasirinkimas bibliotekai, nes visoje sistemoje turi egzistuoti tik vienas centrinis bibliotekos valdymo taškas.

```python
class Library:
    _instance = None

    def __init__(self, name: str):
        if Library._instance is not None:
            raise RuntimeError("Use Library.get_instance()")
        self.__name = name

    @classmethod
    def get_instance(cls, name: str = "City Library"):
        if cls._instance is None:
            cls._instance = cls(name)
        return cls._instance
```

Naudojimas:

```python
lib = Library.get_instance("Vilnius Tech biblioteka")
```

Kiekvieną kartą kviečiant `get_instance()`, grąžinamas tas pats objektas — naujas nekuriamas.

---

### 3. Kompozicija ir agregacija

#### Kompozicija (*Composition*)

`Loan` klasė demonstruoja kompoziciją — ji savyje laiko `LibraryItem` ir `Member` objektus ir be jų neturi prasmės:

```python
class Loan:
    def __init__(self, loan_id: str, item, member: Member):
        self.__loan_id = loan_id
        self.__item = item      
        self.__member = member 
        self.__borrow_date = date.today()
        self.__is_returned = False
```

Skolinimasis neegzistuoja be knygos ir nario.

#### Agregacija (*Aggregation*)

`Library` klasė demonstruoja agregaciją — ji laiko nuorodas į `Book`, `Member` objektus, tačiau šie objektai gali egzistuoti nepriklausomai:

```python
class Library:
    def __init__(self, name: str):
        self.__books = {}   
        self.__members = {}
```

---

### 4. Failų skaitymas ir rašymas

Sistema naudoja CSV formatą duomenims išsaugoti ir užkrauti. Trys failai: `items.csv`, `members.csv`, `loans.csv`.

**Išsaugojimas:**

```python
def save_to_csv(self, directory: str = "data"):
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/items.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "item_id", "title", "year", ...])
        for item in self.__books.values():
            writer.writerow(item.to_csv_row())
```

**Užkrovimas:**

```python
def load_from_csv(self, directory: str = "data"):
    with open(f"{directory}/items.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["type"] == "Book":
                item = Book(row["item_id"], row["title"], ...)
            self.__books[item.item_id] = item
```

Duomenys automatiškai išsaugomi po kiekvieno veiksmo (pridėjimo, skolinimo, grąžinimo).

---

### 5. Testavimas

Projekto testavimui naudojamas Python `unittest` framework. Testai apima visas pagrindines funkcijas:

```python
class TestLibrary(unittest.TestCase):

    def setUp(self):
        Library.reset()
        self.library = Library.get_instance("Test Library")

    def test_borrow_item(self):
        book = Book("B001", "1984", 1949, "Orwell", "000", "Fiction")
        member = Member("P001", "Jonas", "jonas@lt.lt", "MEM-001")
        self.library.add_item(book)
        self.library.register_member(member)
        loan = self.library.borrow_item("B001", "P001")
        self.assertFalse(book.is_available)

    def test_borrow_unavailable_raises(self):
  
        with self.assertRaises(ValueError):
            self.library.borrow_item("B001", "P001") 
```

Iš viso parašyti 28 testai, apimantys: knygų ir žurnalų kūrimą, narių registraciją, skolinimą, grąžinimą, Singleton šabloną, polimorfizmą ir klaidų atvejus.

---

## Rezultatai ir išvados

### Rezultatai

- Sėkmingai įgyvendinti visi 4 OOP principai: abstrakcija, inkapsuliacija, paveldėjimas ir polimorfizmas — kiekvienas aiškiai matomas kode ir turi praktinę paskirtį.
- Singleton dizaino šablonas užtikrina, kad visoje sistemoje egzistuoja tik vienas bibliotekos valdymo objektas, kas apsaugo nuo duomenų nenuoseklumo.
- Didžiausias iššūkis buvo teisingas CSV duomenų užkrovimas paleidžiant programą — reikėjo užtikrinti, kad seni ir nauji duomenys nesusimaišytų.
- Parašyti 28 unit testai, kurie apima visas pagrindines sistemos funkcijas ir leidžia greitai aptikti regresijas keičiant kodą.
- Sistema veikia stabiliai per CLI sąsają ir automatiškai išsaugo duomenis po kiekvieno veiksmo.

### Išvados

Šio kursinio darbo metu sukurta funkcionali bibliotekos valdymo sistema, demonstruojanti visus pagrindinius objektinio programavimo principus. Programos rezultatas — stabili CLI sistema, leidžianti valdyti knygas, žurnalus, narius ir skolinimus su nuolatiniu duomenų saugojimu.

Ateityje programą būtų galima išplėsti:

- Duomenų bazė — pakeisti CSV failus į SQLite arba PostgreSQL duomenų bazę.
- Paieška pagal autorių — išplėsti paieškos funkcionalumą.
- Skolinimo terminas — pridėti grąžinimo terminą ir baudas už pavėlavimą.
- El. pašto priminimai — automatiškai siųsti priminimus nariam prieš pasibaigiant skolinimo terminui.

---

## Šaltiniai

- Python dokumentacija: https://docs.python.org/3/
- PEP 8 stilius: https://pep8.org/
- ABC modulis: https://docs.python.org/3/library/abc.html
- unittest: https://docs.python.org/3/library/unittest.html
- Dizaino šablonai: https://refactoring.guru/design-patterns
- CSV modulis: https://docs.python.org/3/library/csv.html
- OOP teorija: https://oop.szturo.online/
