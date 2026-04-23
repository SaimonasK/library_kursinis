from abc import ABC, abstractmethod

class LibraryItem(ABC):

    def __init__(self, item_id: str, title: str, year: int):
        self.__item_id = item_id       
        self.__title = title
        self.__year = year
        self.__is_available = True

    @property
    def item_id(self) -> str:
        return self.__item_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def year(self) -> int:
        return self.__year

    @property
    def is_available(self) -> bool:
        return self.__is_available

    @is_available.setter
    def is_available(self, value: bool):
        self.__is_available = value

    @abstractmethod
    def get_info(self) -> str:
        pass

    def __str__(self) -> str:
        status = "available" if self.__is_available else "borrowed"
        return f"[{self.__item_id}] {self.__title} ({self.__year}) — {status}"


class Person(ABC):

    def __init__(self, person_id: str, name: str, email: str):
        self.__person_id = person_id
        self.__name = name
        self.__email = email

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address.")
        self.__email = value

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self) -> str:
        return f"[{self.__person_id}] {self.__name} ({self.get_role()})"
