from models.items import Book, Magazine
from models.people import Member, Librarian
from library import Library


def print_separator():
    print("-" * 40)


def menu_add_book(lib):
    print("\n--- Add Book ---")
    item_id = input("ID (e.g. B001): ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = int(input("Year: ").strip())
    isbn = input("ISBN: ").strip()
    genre = input("Genre: ").strip()
    try:
        lib.add_item(Book(item_id, title, year, author, isbn, genre))
        print(f"Book '{title}' added.")
        lib.save_to_csv("data")
    except ValueError as e:
        print(f"Error: {e}")


def menu_add_magazine(lib):
    print("\n--- Add Magazine ---")
    item_id = input("ID (e.g. M001): ").strip()
    title = input("Title: ").strip()
    year = int(input("Year: ").strip())
    issue = int(input("Issue number: ").strip())
    publisher = input("Publisher: ").strip()
    try:
        lib.add_item(Magazine(item_id, title, year, issue, publisher))
        print(f"Magazine '{title}' added.")
        lib.save_to_csv("data")
    except ValueError as e:
        print(f"Error: {e}")


def menu_register_member(lib):
    print("\n--- Register Member ---")
    person_id = input("Person ID (e.g. P001): ").strip()
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    membership_id = input("Membership ID (e.g. MEM-001): ").strip()
    try:
        lib.register_member(Member(person_id, name, email, membership_id))
        print(f"Member '{name}' registered.")
        lib.save_to_csv("data")
    except (ValueError, Exception) as e:
        print(f"Error: {e}")


def menu_borrow(lib):
    print("\n--- Borrow Item ---")
    item_id = input("Item ID: ").strip()
    member_id = input("Member person ID: ").strip()
    try:
        loan = lib.borrow_item(item_id, member_id)
        print(f"Success! {loan}")
        lib.save_to_csv("data")
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")


def menu_return(lib):
    print("\n--- Return Item ---")
    loan_id = input("Loan ID (e.g. L0001): ").strip()
    try:
        loan = lib.return_item(loan_id)
        print(f"Returned: {loan}")
        lib.save_to_csv("data")
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")


def menu_list_items(lib):
    print("\n--- All Available Items ---")
    items = lib.list_available_items()
    if not items:
        print("No items available.")
    for item in items:
        print(f"ID: {item.item_id}")
        print(item.get_info())
        print()


def menu_search(lib):
    print("\n--- Search Items ---")
    query = input("Search by title: ").strip()
    results = lib.search_items(query)
    if not results:
        print("No results found.")
    for item in results:
        print(item)


def menu_list_loans(lib):
    print("\n--- Active Loans ---")
    loans = lib.list_active_loans()
    if not loans:
        print("No active loans.")
    for loan in loans:
        print(loan)


def menu_list_members(lib):
    print("\n--- Members ---")
    members = lib.list_members()
    if not members:
        print("No members registered.")
    for m in members:
        print(m.get_info())
        print()


def main():
    lib = Library.get_instance("Vilnius Tech biblioteka")

    # Try loading existing data
    try:
        lib.load_from_csv("data")
    except Exception:
        pass

    while True:
        print("\n" + "=" * 40)
        print(lib)
        print("=" * 40)
        print("1. List available items")
        print("2. Search items")
        print("3. Add book")
        print("4. Add magazine")
        print("5. Register member")
        print("6. List members")
        print("7. Borrow item")
        print("8. Return item")
        print("9. List active loans")
        print("s. Save to CSV")
        print("q. Quit")
        print_separator()

        choice = input("Choose: ").strip().lower()

        if choice == "1":
            menu_list_items(lib)
        elif choice == "2":
            menu_search(lib)
        elif choice == "3":
            menu_add_book(lib)
        elif choice == "4":
            menu_add_magazine(lib)
        elif choice == "5":
            menu_register_member(lib)
        elif choice == "6":
            menu_list_members(lib)
        elif choice == "7":
            menu_borrow(lib)
        elif choice == "8":
            menu_return(lib)
        elif choice == "9":
            menu_list_loans(lib)
        elif choice == "s":
            lib.save_to_csv("data")
        elif choice == "q":
            lib.save_to_csv("data")
            print("Data saved. Bye!")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()