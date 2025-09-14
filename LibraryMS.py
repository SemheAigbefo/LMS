from Librarydb import add_book_to_db, remove_book_from_db_by_isbn, search_books_in_db, get_books_from_db, get_book_count

class Book:
    def __init__(self, title, author, isbn, pub, status="available", due_date=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pub = pub
        self.status = status
        self.due_date = due_date
    
    def save_to_db(self):
        return add_book_to_db(self)

class Member:
    def __init__(self, name, id, contact, borrowed, checkout):
        self.name = name
        self.id = id
        self.contact = contact
        self.borrowed = borrowed
        self.checkout = checkout

class Librarian:
    def __init__(self, name, id):
        self.name = name
        self.id = str(id).strip()  # Ensure id is a string and stripped

    def check_librarian(self):
        try:
            with open("librarians.txt", "r") as f:
                allowed_ids = [line.strip() for line in f if line.strip()]
            return self.id in allowed_ids
        except Exception as e:
            print("Error reading librarians.txt:", e)
            return False

class Library:
    def __init__(self):
        self.books = []
        self.load_books()
    
    def load_books(self):
        try:
            book_data = get_books_from_db()
            self.books = [Book(*data) for data in book_data]
        except Exception as e:
            print("Error loading books:", e)
            self.books = []
    
    def display_books(self):
        print("\nLibrary Books:")
        print("-" * 80)
        print(f"{'No.':<4} {'Title':<25} {'Author':<20} {'ISBN':<15} {'Status':<10}")
        print("-" * 80)
        
        for i, book in enumerate(self.books, 1):
            print(f"{i:<4} {book.title:<25} {book.author:<20} {book.isbn:<15} {book.status:<10}")
        
        print("-" * 80)

# Main program
def librarian_menu(library):
    lib_name = input("Enter librarian name: ")
    lib_id = input("Enter librarian ID: ")
    librarian = Librarian(lib_name, lib_id)
    if not librarian.check_librarian():
        print(f"Access denied. '{librarian.name}' is not an authorized librarian.")
        return

    print(f"Welcome, Librarian {librarian.name}!")
    
    while True:
        print("\nLibrarian Menu:")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            pub_year = input("Enter publication year: ")
            
            new_book = Book(title, author, isbn, pub_year)
            if new_book.save_to_db():
                print("Book added successfully!")
                library.load_books()  # Reload books from database
            else:
                print("Failed to add book.")
        
        elif choice == "2":
            isbn = input("Enter ISBN of the book to remove: ")
            if remove_book_from_db_by_isbn(isbn):
                print("Book removed successfully!")
                library.load_books()  # Reload books from database
            else:
                print("Failed to remove book.")
        
        elif choice == "3":
            search_type = int(input("Search by: 1 for Title, 2 for ISBN: "))
            if search_type == 1:
                search_value = input("Enter book title: ")
            else:
                search_value = input("Enter ISBN: ")
            
            results = search_books_in_db(search_type, search_value)
            if results:
                print("\nSearch Results:")
                print("-" * 80)
                for book in results:
                    print(f"Title: {book[0]}, Author: {book[2]}, ISBN: {book[1]}, Status: {book[4]}")
                print("-" * 80)
            else:
                print("No books found.")
        
        elif choice == "4":
            library.display_books()
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

def member_menu(library):
    print("Welcome, Member!")
    library.display_books()

def main():
    library = Library()
    
    while True:
        person = input("Are you a Librarian or Member? (or type 'exit' to quit): ").strip().lower()
        
        if person == "librarian":
            librarian_menu(library)
        elif person == "member":
            member_menu(library)
        elif person == "exit":
            print("Goodbye!")
            break
        else:
            print("Please enter either 'Librarian' or 'Member'.")

if __name__ == "__main__":
    main()