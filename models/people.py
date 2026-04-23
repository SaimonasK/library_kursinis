from datetime import date
from models.base import Person
from models.items import Book, Magazine


class Member(Person):
    def __init__(self, person_id: str, name: str, email: str, membership_id: str):
        super().__init__(person_id, name, email)
        self.__membership_id = membership_id
        self.__borrowed_items = []

    @property
    def membership_id(self) -> str:
        return self.__membership_id

    @property
    def borrowed_items(self) -> list:
        return list(self.__borrowed_items)

    def add_borrowed(self, item):
        self.__borrowed_items.append(item)

    def remove_borrowed(self, item):
        self.__borrowed_items.remove(item)

    def get_role(self) -> str:
        return "Member"

    def get_info(self) -> str:
        borrowed_titles = [item.title for item in self.__borrowed_items]
        return (
            f"Member | {self.name}\n"
            f"  Person ID  : {self.person_id}\n"
            f"  Membership : {self.membership_id}\n"
            f"  Email      : {self.email}\n"
            f"  Borrowed   : {borrowed_titles if borrowed_titles else 'none'}"
        )

    def to_csv_row(self) -> list:
        return ["Member", self.person_id, self.name, self.email, self.__membership_id]


class Librarian(Person):
    def __init__(self, person_id: str, name: str, email: str, employee_id: str):
        super().__init__(person_id, name, email)
        self.__employee_id = employee_id

    @property
    def employee_id(self) -> str:
        return self.__employee_id

    def get_role(self) -> str:
        return "Librarian"

    def to_csv_row(self) -> list:
        return ["Librarian", self.person_id, self.name, self.email, self.__employee_id]


class Loan:

    def __init__(self, loan_id: str, item, member: Member):
        self.__loan_id = loan_id
        self.__item = item
        self.__member = member
        self.__borrow_date = date.today()
        self.__return_date = None
        self.__is_returned = False

    @property
    def loan_id(self) -> str:
        return self.__loan_id

    @property
    def item(self):
        return self.__item

    @property
    def member(self) -> Member:
        return self.__member

    @property
    def borrow_date(self) -> date:
        return self.__borrow_date

    @property
    def return_date(self):
        return self.__return_date

    @property
    def is_returned(self) -> bool:
        return self.__is_returned

    def complete_return(self):
        self.__is_returned = True
        self.__return_date = date.today()

    def __str__(self) -> str:
        status = f"returned {self.__return_date}" if self.__is_returned else "active"
        return (
            f"Loan [{self.__loan_id}] | {self.__item.title} → {self.__member.name} "
            f"| borrowed: {self.__borrow_date} | {status}"
        )

    def to_csv_row(self) -> list:
        return [
            self.__loan_id,
            self.__item.item_id,
            self.__member.person_id,
            self.__borrow_date,
            self.__return_date if self.__return_date else "",
            self.__is_returned
        ]
