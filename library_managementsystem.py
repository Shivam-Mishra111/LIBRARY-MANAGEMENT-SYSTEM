# library_system.py

class Book:
    def __init__(self, book_id, title, author, total_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def __str__(self):
        return f"[{self.book_id}] {self.title} by {self.author} | Available: {self.available_copies}/{self.total_copies}"


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def __str__(self):
        return f"[{self.member_id}] {self.name}"


class Library:
    def __init__(self):
        self.books = {}      # book_id -> Book
        self.members = {}    # member_id -> Member
        self.loans = []      # list of dicts: {"member_id": ..., "book_id": ...}

    # ---------- BOOK METHODS ----------

    def add_book(self, title, author, total_copies):
        if total_copies <= 0:
            return False, "Total copies must be positive."

        book_id = len(self.books) + 1
        self.books[book_id] = Book(book_id, title, author, total_copies)
        return True, f"Book added with ID {book_id}"

    def list_books(self):
        if not self.books:
            print("No books in the library.")
            return
        print("\n--- Book List ---")
        for book in self.books.values():
            print(book)

    def search_books(self, keyword):
        keyword = keyword.lower()
        results = [
            book for book in self.books.values()
            if keyword in book.title.lower() or keyword in book.author.lower()
        ]
        if not results:
            print("No matching books found.")
            return
        print("\n--- Search Results ---")
        for book in results:
            print(book)

    # ---------- MEMBER METHODS ----------

    def add_member(self, name):
        if not name.strip():
            return False, "Member name cannot be empty."

        member_id = len(self.members) + 1
        self.members[member_id] = Member(member_id, name.strip())
        return True, f"Member added with ID {member_id}"

    def list_members(self):
        if not self.members:
            print("No members registered.")
            return
        print("\n--- Member List ---")
        for member in self.members.values():
            print(member)

    # ---------- LOAN METHODS ----------

    def borrow_book(self, member_id, book_id):
        if member_id not in self.members:
            return False, "Member not found."
        if book_id not in self.books:
            return False, "Book not found."

        book = self.books[book_id]
        if book.available_copies <= 0:
            return False, "No copies available for this book."

        # Check if member already borrowed this book
        for loan in self.loans:
            if loan["member_id"] == member_id and loan["book_id"] == book_id:
                return False, "Member has already borrowed this book."

        book.available_copies -= 1
        self.loans.append({"member_id": member_id, "book_id": book_id})
        return True, "Book issued successfully."

    def return_book(self, member_id, book_id):
        for loan in self.loans:
            if loan["member_id"] == member_id and loan["book_id"] == book_id:
                self.loans.remove(loan)
                self.books[book_id].available_copies += 1
                return True, "Book returned successfully."
        return False, "No such loan record found."

    def list_loans(self):
        if not self.loans:
            print("No books are currently issued.")
            return

        print("\n--- Issued Books ---")
        for loan in self.loans:
            member = self.members[loan["member_id"]]
            book = self.books[loan["book_id"]]
            print(f"Member: {member.name} (ID: {member.member_id}) "
                  f"=> Book: {book.title} (ID: {book.book_id})")


# ---------- USER INTERFACE ----------

def print_menu():
    print("\n========== Library Management System ==========")
    print("1. Add Book")
    print("2. Add Member")
    print("3. List Books")
    print("4. List Members")
    print("5. Search Books")
    print("6. Issue Book")
    print("7. Return Book")
    print("8. View Issued Books")
    print("0. Exit")
    print("===============================================")


def main():
    library = Library()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            try:
                total = int(input("Enter total copies: "))
            except ValueError:
                print("Total copies must be a number.")
                continue
            success, msg = library.add_book(title, author, total)
            print(msg)

        elif choice == "2":
            name = input("Enter member name: ")
            success, msg = library.add_member(name)
            print(msg)

        elif choice == "3":
            library.list_books()

        elif choice == "4":
            library.list_members()

        elif choice == "5":
            keyword = input("Enter title/author keyword to search: ")
            library.search_books(keyword)

        elif choice == "6":
            try:
                member_id = int(input("Enter member ID: "))
                book_id = int(input("Enter book ID: "))
            except ValueError:
                print("IDs must be numbers.")
                continue
            success, msg = library.borrow_book(member_id, book_id)
            print(msg)

        elif choice == "7":
            try:
                member_id = int(input("Enter member ID: "))
                book_id = int(input("Enter book ID: "))
            except ValueError:
                print("IDs must be numbers.")
                continue
            success, msg = library.return_book(member_id, book_id)
            print(msg)

        elif choice == "8":
            library.list_loans()

        elif choice == "0":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
