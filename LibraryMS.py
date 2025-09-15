"""
Library Management System Main Module

This module contains the main application logic for the Library Management System,
including the Book and Librarian classes, Library management, and user interface menus.
"""

from Librarydb import add_book_to_db, remove_book_from_db_by_isbn, search_books_in_db, get_books_from_db, get_book_count, verify_librarian_id


class Book:
    """Represents a book in the library system with all relevant metadata."""
    
    def __init__(self, title, author, isbn, pub, status="available", due_date=None):
        """
        Initialize a Book instance.
        
        Args:
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): International Standard Book Number
            pub (str): Publication year
            status (str): Availability status, defaults to "available"
            due_date (str): Due date if borrowed, defaults to None
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pub = pub
        self.status = status
        self.due_date = due_date
    
    def save_to_db(self):
        """
        Save the book to the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        return add_book_to_db(self)


class Librarian:
    """Represents a librarian with authentication capabilities."""
    
    def __init__(self, name, id):
        """
        Initialize a Librarian instance.
        
        Args:
            name (str): Librarian's name
            id (str/int): Librarian identification number
        """
        self.name = name
        self.id = str(id).strip()

    def check_librarian(self):
        """
        Verify librarian credentials against authorized list.
        
        Returns:
            bool: True if librarian ID is authorized, False otherwise
        """
        try:
            with open("librarians.txt", "r") as f:
                allowed_ids = [line.strip() for line in f if line.strip()]
            return self.id in allowed_ids
        except Exception as e:
            print("Error reading librarians.txt:", e)
            return False


class Library:
    """Main library class managing book collection and operations."""
    
    def __init__(self):
        """Initialize Library instance and load books from database."""
        self.books = []
        self.load_books()
    
    def load_books(self):
        """Load all books from the database into memory."""
        try:
            book_data = get_books_from_db()
            self.books = [Book(*data) for data in book_data]
        except Exception as e:
            print("Error loading books:", e)
            self.books = []
    
    def display_books(self):
        """Display all books in a formatted table."""
        print("\nLibrary Books:")
        print("-" * 80)
        print(f"{'No.':<4} {'Title':<25} {'Author':<20} {'ISBN':<15} {'Status':<10}")
        print("-" * 80)
        
        for i, book in enumerate(self.books, 1):
            print(f"{i:<4} {book.title:<25} {book.author:<20} {book.isbn:<15} {book.status:<10}")
        
        print("-" * 80)


def librarian_menu(library):
    """
    Display and handle the librarian menu interface.
    
    Args:
        library (Library): The library instance to operate on
    """
    lib_id = input("Enter librarian ID: ")
    
    if not verify_librarian_id(lib_id):
        print("Access denied")
        return
    
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
            isbn = input("Enter ISBN: ")
            author = input("Enter author: ")
            pub_year = input("Enter publication year: ")
            
            new_book = Book(title, author, isbn, pub_year)
            if new_book.save_to_db():
                print("Book added successfully!")
                library.load_books()
            else:
                print("Failed to add book.")
        
        elif choice == "2":
            isbn = input("Enter ISBN of the book to remove: ")
            if remove_book_from_db_by_isbn(isbn):
                print("Book removed successfully!")
                library.load_books()
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
    """
    Display and handle the member menu interface.
    
    Args:
        library (Library): The library instance to operate on
    """
    print("Welcome, Member!")
    actions = int(input("Press 1 to load all books \nPress 2 to search a book\n"))
    
    if actions == 1:
        library.display_books()
    elif actions == 2:
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
            print("Contact the librarian at the front desk for checkout or checkout details\n")
        else:
            print("No books found.")


def main():
    """
    Main application entry point.
    
    Initializes the library system and handles user role selection
    through the main menu interface.
    """
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