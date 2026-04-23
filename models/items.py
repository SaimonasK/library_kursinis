from models.base import LibraryItem

class Book(LibraryItem):

    def __init__(self, item_id: str, title: str, year: int, author: str, isbn: str, genre: str):
        super().__init__(item_id, title, year)
        self.__author = author         
        self.__isbn = isbn
        self.__genre = genre

    @property
    def author(self) -> str:
        return self.__author

    @property
    def isbn(self) -> str:
        return self.__isbn

    @property
    def genre(self) -> str:
        return self.__genre

    def get_info(self) -> str:
        status = "Available" if self.is_available else "Borrowed"
        return (
            f"Book | {self.title}\n"
            f"  Author : {self.__author}\n"
            f"  ISBN   : {self.__isbn}\n"
            f"  Genre  : {self.__genre}\n"
            f"  Year   : {self.year}\n"
            f"  Status : {status}"
        )

    def to_csv_row(self) -> list:
        return [
            "Book", self.item_id, self.title, self.year,
            self.__author, self.__isbn, self.__genre, self.is_available
        ]


class Magazine(LibraryItem):

    def __init__(self, item_id: str, title: str, year: int, issue_number: int, publisher: str):
        super().__init__(item_id, title, year)
        self.__issue_number = issue_number
        self.__publisher = publisher

    @property
    def issue_number(self) -> int:
        return self.__issue_number

    @property
    def publisher(self) -> str:
        return self.__publisher

    def get_info(self) -> str:
        status = "Available" if self.is_available else "Borrowed"
        return (
            f"Magazine | {self.title}\n"
            f"  Issue     : #{self.__issue_number}\n"
            f"  Publisher : {self.__publisher}\n"
            f"  Year      : {self.year}\n"
            f"  Status    : {status}"
        )

    def to_csv_row(self) -> list:
        return [
            "Magazine", self.item_id, self.title, self.year,
            "", str(self.__issue_number), self.__publisher, self.is_available
        ]
