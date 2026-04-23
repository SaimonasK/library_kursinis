import csv
import os
from models.items import Book, Magazine
from models.people import Member, Librarian, Loan


class Library:

    _instance = None

    def __init__(self, name: str):
        if Library._instance is not None:
            raise RuntimeError("Use Library.get_instance() to access the library.")
        self.__name = name
        self.__books = {}     
        self.__members = {}
        self.__loans = {}       
        self.__loan_counter = 1

    @classmethod
    def get_instance(cls, name: str = "City Library"):
        if cls._instance is None:
            cls._instance = cls(name)
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None



    def add_item(self, item):
        if item.item_id in self.__books:
            raise ValueError(f"Item with ID '{item.item_id}' already exists.")
        self.__books[item.item_id] = item

    def remove_item(self, item_id: str):
        if item_id not in self.__books:
            raise KeyError(f"Item '{item_id}' not found.")
        del self.__books[item_id]

    def get_item(self, item_id: str):
        if item_id not in self.__books:
            raise KeyError(f"Item '{item_id}' not found.")
        return self.__books[item_id]

    def search_items(self, query: str) -> list:
        query = query.lower()
        return [
            item for item in self.__books.values()
            if query in item.title.lower()
        ]

    def list_available_items(self) -> list:
        return [item for item in self.__books.values() if item.is_available]



    def register_member(self, member: Member):
        if member.person_id in self.__members:
            raise ValueError(f"Member '{member.person_id}' already registered.")
        self.__members[member.person_id] = member

    def get_member(self, person_id: str) -> Member:
        if person_id not in self.__members:
            raise KeyError(f"Member '{person_id}' not found.")
        return self.__members[person_id]

    def list_members(self) -> list:
        return list(self.__members.values())



    def borrow_item(self, item_id: str, member_id: str) -> Loan:
        item = self.get_item(item_id)
        member = self.get_member(member_id)

        if not item.is_available:
            raise ValueError(f"'{item.title}' is currently not available.")

        loan_id = f"L{self.__loan_counter:04d}"
        self.__loan_counter += 1

        loan = Loan(loan_id, item, member)
        item.is_available = False
        member.add_borrowed(item)
        self.__loans[loan_id] = loan
        return loan

    def return_item(self, loan_id: str) -> Loan:
        if loan_id not in self.__loans:
            raise KeyError(f"Loan '{loan_id}' not found.")
        loan = self.__loans[loan_id]

        if loan.is_returned:
            raise ValueError(f"Loan '{loan_id}' is already returned.")

        loan.complete_return()
        loan.item.is_available = True
        loan.member.remove_borrowed(loan.item)
        return loan

    def list_active_loans(self) -> list:
        return [loan for loan in self.__loans.values() if not loan.is_returned]



    def save_to_csv(self, directory: str = "data"):
        os.makedirs(directory, exist_ok=True)

        with open(f"{directory}/items.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["type", "item_id", "title", "year", "field1", "field2", "field3", "is_available"])
            for item in self.__books.values():
                writer.writerow(item.to_csv_row())

        with open(f"{directory}/members.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["role", "person_id", "name", "email", "extra_id"])
            for member in self.__members.values():
                writer.writerow(member.to_csv_row())

        with open(f"{directory}/loans.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["loan_id", "item_id", "member_id", "borrow_date", "return_date", "is_returned"])
            for loan in self.__loans.values():
                writer.writerow(loan.to_csv_row())

        print(f"Data saved to '{directory}/'.")

    def load_from_csv(self, directory: str = "data"):
        items_path = f"{directory}/items.csv"
        members_path = f"{directory}/members.csv"

        if os.path.exists(items_path):
            with open(items_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["type"] == "Book":
                        item = Book(
                            row["item_id"], row["title"], int(row["year"]),
                            row["field1"], row["field2"], row["field3"]
                        )
                    elif row["type"] == "Magazine":
                        item = Magazine(
                            row["item_id"], row["title"], int(row["year"]),
                            int(row["field2"]), row["field3"]
                        )
                    else:
                        continue
                    item.is_available = row["is_available"] == "True"
                    self.__books[item.item_id] = item

        if os.path.exists(members_path):
            with open(members_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["role"] == "Member":
                        member = Member(
                            row["person_id"], row["name"], row["email"], row["extra_id"]
                        )
                        self.__members[member.person_id] = member

        print(f"Data loaded from '{directory}/'.")



    def __str__(self) -> str:
        return (
            f"=== {self.__name} ===\n"
            f"Items: {len(self.__books)} | Members: {len(self.__members)} | "
            f"Active loans: {len(self.list_active_loans())}"
        )
