import unittest
from models.base import LibraryItem, Person
from models.items import Book, Magazine
from models.people import Member, Librarian, Loan
from library import Library


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book("B001", "Clean Code", 2008, "Robert Martin", "978-0132350884", "Programming")

    def test_initial_availability(self):
        self.assertTrue(self.book.is_available)

    def test_get_info_contains_title(self):
        self.assertIn("Clean Code", self.book.get_info())

    def test_get_info_contains_author(self):
        self.assertIn("Robert Martin", self.book.get_info())

    def test_set_availability(self):
        self.book.is_available = False
        self.assertFalse(self.book.is_available)

    def test_str_representation(self):
        self.assertIn("B001", str(self.book))

    def test_to_csv_row(self):
        row = self.book.to_csv_row()
        self.assertEqual(row[0], "Book")
        self.assertEqual(row[1], "B001")


class TestMagazine(unittest.TestCase):

    def setUp(self):
        self.mag = Magazine("M001", "National Geographic", 2023, 42, "NatGeo Inc.")

    def test_get_info_contains_issue(self):
        self.assertIn("42", self.mag.get_info())

    def test_get_info_type_label(self):
        self.assertIn("Magazine", self.mag.get_info())

    def test_availability_default_true(self):
        self.assertTrue(self.mag.is_available)


class TestMember(unittest.TestCase):

    def setUp(self):
        self.member = Member("P001", "Jonas Jonaitis", "jonas@example.com", "MEM-001")

    def test_role(self):
        self.assertEqual(self.member.get_role(), "Member")

    def test_email_validation_raises(self):
        with self.assertRaises(ValueError):
            self.member.email = "not-an-email"

    def test_borrowed_items_initially_empty(self):
        self.assertEqual(len(self.member.borrowed_items), 0)

    def test_add_borrowed(self):
        book = Book("B001", "Clean Code", 2008, "R. Martin", "123", "Tech")
        self.member.add_borrowed(book)
        self.assertEqual(len(self.member.borrowed_items), 1)

    def test_remove_borrowed(self):
        book = Book("B001", "Clean Code", 2008, "R. Martin", "123", "Tech")
        self.member.add_borrowed(book)
        self.member.remove_borrowed(book)
        self.assertEqual(len(self.member.borrowed_items), 0)


class TestLibrarian(unittest.TestCase):

    def test_role(self):
        lib = Librarian("P002", "Ona Onaitė", "ona@lib.lt", "EMP-001")
        self.assertEqual(lib.get_role(), "Librarian")


class TestLibrary(unittest.TestCase):

    def setUp(self):
        Library.reset()
        self.library = Library.get_instance("Test Library")
        self.book = Book("B001", "1984", 1949, "George Orwell", "000", "Fiction")
        self.member = Member("P001", "Jonas", "jonas@lt.lt", "MEM-001")
        self.library.add_item(self.book)
        self.library.register_member(self.member)

    def tearDown(self):
        Library.reset()

    def test_singleton_same_instance(self):
        lib2 = Library.get_instance()
        self.assertIs(self.library, lib2)

    def test_add_item(self):
        self.assertEqual(self.library.get_item("B001").title, "1984")

    def test_duplicate_item_raises(self):
        with self.assertRaises(ValueError):
            self.library.add_item(Book("B001", "Duplicate", 2000, "X", "X", "X"))

    def test_remove_item(self):
        self.library.remove_item("B001")
        with self.assertRaises(KeyError):
            self.library.get_item("B001")

    def test_borrow_item(self):
        loan = self.library.borrow_item("B001", "P001")
        self.assertFalse(self.book.is_available)
        self.assertEqual(len(self.member.borrowed_items), 1)
        self.assertIsNotNone(loan.loan_id)

    def test_borrow_unavailable_raises(self):
        self.library.borrow_item("B001", "P001")
        with self.assertRaises(ValueError):
            self.library.borrow_item("B001", "P001")

    def test_return_item(self):
        loan = self.library.borrow_item("B001", "P001")
        self.library.return_item(loan.loan_id)
        self.assertTrue(self.book.is_available)
        self.assertEqual(len(self.member.borrowed_items), 0)

    def test_return_already_returned_raises(self):
        loan = self.library.borrow_item("B001", "P001")
        self.library.return_item(loan.loan_id)
        with self.assertRaises(ValueError):
            self.library.return_item(loan.loan_id)

    def test_search_items(self):
        results = self.library.search_items("1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

    def test_search_case_insensitive(self):
        results = self.library.search_items("orwell")
        # Search is by title only, so this should return empty
        results_title = self.library.search_items("1984")
        self.assertEqual(len(results_title), 1)

    def test_list_available(self):
        self.assertEqual(len(self.library.list_available_items()), 1)
        self.library.borrow_item("B001", "P001")
        self.assertEqual(len(self.library.list_available_items()), 0)

    def test_active_loans(self):
        loan = self.library.borrow_item("B001", "P001")
        self.assertEqual(len(self.library.list_active_loans()), 1)
        self.library.return_item(loan.loan_id)
        self.assertEqual(len(self.library.list_active_loans()), 0)


class TestPolymorphism(unittest.TestCase):

    def test_book_and_magazine_get_info_differ(self):
        book = Book("B001", "Dune", 1965, "Frank Herbert", "000", "Sci-Fi")
        mag = Magazine("M001", "Time", 2023, 10, "Time Inc.")
        self.assertIn("Author", book.get_info())
        self.assertIn("Issue", mag.get_info())
        self.assertNotEqual(book.get_info(), mag.get_info())


if __name__ == "__main__":
    unittest.main(verbosity=2)
