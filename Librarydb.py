"""
Library Management System Database Module

This module handles all database operations for the Library Management System,
including database creation, initialization, and CRUD operations for books
and librarians. Uses PostgreSQL as the backend database.
"""

import os
import psycopg2


def create_database():
    """
    Create the LMS database if it doesn't exist.
    
    Connects to the default PostgreSQL database and creates the 'lms' database
    if it doesn't already exist. This function should be called before any
    other database operations.
    
    Raises:
        Exception: If database creation fails due to connection issues or
                   insufficient permissions.
    """
    try:
        # Connect to the default PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",  # Connect to default database
            user="postgres",
            password="postgreSem",
            port=5432
        )
        conn.autocommit = True  # Required for creating databases
        cur = conn.cursor()
        
        # Check if database exists and create if it doesn't
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'lms'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute("CREATE DATABASE lms")
            print("Database 'lms' created successfully")
        
        cur.close()
        conn.close()
    except Exception as e:
        print("Error creating database:", e)


# Call this function before your main database operations
create_database()


def get_db_connection():
    """
    Establish and return a connection to the LMS database.
    
    Uses environment variables for database configuration with fallback
    to default values. Handles connection errors gracefully.
    
    Returns:
        psycopg2.connection: Database connection object if successful,
        None if connection fails.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'lms'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgreSem'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


def init_database():
    """
    Initialize the database schema with required tables and sample data.
    
    Creates LIBRARIAN and BOOK tables if they don't exist and populates
    them with initial sample data. Includes conflict handling to prevent
    duplicate entries on subsequent runs.
    
    Raises:
        Exception: If table creation or data insertion fails.
    """
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        cur = conn.cursor()
        
        # Create tables if they don't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS LIBRARIAN (
                name TEXT NOT NULL,
                id INT PRIMARY KEY
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS BOOK (
                name TEXT NOT NULL,
                Author TEXT NOT NULL,
                ISBN BIGINT PRIMARY KEY NOT NULL,
                Pub_Year INT NOT NULL,
                Availability TEXT DEFAULT 'Available'
            )
        """)
        
        # Insert sample librarians
        cur.execute("""
            INSERT INTO LIBRARIAN (name, id)
            VALUES 
                ('Chloe Smith', 70552),
                ('Ben Carter', 70704), 
                ('Alice Johnson', 70895)
            ON CONFLICT (id) DO NOTHING  -- Prevents duplicates
        """)
        
        # Insert sample books (optional)
        cur.execute("""
            INSERT INTO BOOK (name, Author, ISBN, Pub_Year, Availability)
            VALUES
                ('Python Programming', 'John Doe', 9780123456789, 2023, 'Available'),
                ('Database Systems', 'Jane Smith', 9780987654321, 2022, 'Available'),
                ('Web Development', 'Mike Johnson', 9781234567890, 2024, 'Borrowed')
            ON CONFLICT (ISBN) DO NOTHING  -- Prevents duplicates
        """)
        
        conn.commit()
        print("Database initialized with sample data successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


init_database()


def verify_librarian_id(l_id):
    """
    Verify if a librarian ID exists in the database and return their name.
    
    Args:
        l_id (int): The librarian ID to verify.
        
    Returns:
        str: The librarian's name if found, None if not found.
        
    Raises:
        Exception: If database query fails.
    """
    conn = get_db_connection()
    if conn is None:
        return []
    
    try:
        cur = conn.cursor()

        cur.execute("SELECT name FROM LIBRARIAN WHERE id = %s", (l_id,))
        result = cur.fetchone()

        librarian_name = result[0] if result else None
        print ("Hello, "+librarian_name)
        return librarian_name  
      
    except Exception as e:
        print("Error searching for librarian id:", e)
        return []
    finally:
        conn.close()


def add_book_to_db(book):
    """
    Add a new book to the database.
    
    Args:
        book (Book): A Book object containing title, author, ISBN, 
                    publication year, and availability status.
                    
    Returns:
        bool: True if book was added successfully, False otherwise.
        
    Raises:
        Exception: If database insertion fails.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO BOOK (name, ISBN, Author, Pub_Year, Availability)
            VALUES (%s, %s, %s, %s, %s)
        """, (book.title, book.isbn, book.author, book.pub, book.status))
        
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print("Error adding book to database:", e)
        return False
    finally:
        conn.close()


def search_books_in_db(search_type, search_value):
    """
    Search for books in the database by name or ISBN.
    
    Args:
        search_type (int): 1 to search by name, 2 to search by ISBN.
        search_value (str): The search term (book name or ISBN).
        
    Returns:
        list: List of matching book records, empty list if no matches found.
        
    Raises:
        Exception: If database query fails.
    """
    conn = get_db_connection()
    if conn is None:
        return []
    
    try:
        cur = conn.cursor()
        if search_type == 1:  # Search by name
            cur.execute("SELECT * FROM BOOK WHERE name ILIKE %s", (f'%{search_value}%',))
        else:  # Search by ISBN
            cur.execute("SELECT * FROM BOOK WHERE ISBN = %s", (search_value,))
        
        books = cur.fetchall()
        cur.close()
        return books
    except Exception as e:
        print("Error searching books:", e)
        return []
    finally:
        conn.close()


def remove_book_from_db_by_isbn(isbn):
    """
    Remove a book from the database by its ISBN.
    
    Args:
        isbn (int): The ISBN of the book to remove.
        
    Returns:
        bool: True if book was removed successfully, False if book not found
              or removal failed.
              
    Raises:
        Exception: If database deletion fails.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cur = conn.cursor()
        # First check if the book exists
        cur.execute("SELECT * FROM BOOK WHERE ISBN = %s", (isbn,))
        book = cur.fetchone()
        
        if not book:
            print(f"Book with ISBN {isbn} not found!")
            return False
        
        # Delete the book
        cur.execute("DELETE FROM BOOK WHERE ISBN = %s", (isbn,))
        
        conn.commit()
        cur.close()
        print(f"Book with ISBN {isbn} successfully removed from database!")
        return True
        
    except Exception as e:
        print("Error removing book from database:", e)
        return False
    finally:
        conn.close()


def get_books_from_db():
    """
    Retrieve all books from the database sorted by name.
    
    Returns:
        list: List of all book records, None if error occurs.
        
    Raises:
        Exception: If database query fails.
    """
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BOOK ORDER BY name")
        books = cur.fetchall()
        cur.close()
        return books
        
    except Exception as e:
        print("Error getting books from database:", e)
        return None
    finally:
        conn.close()


def get_book_count():
    """
    Get the total number of books in the database.
    
    Returns:
        int: Total count of books, 0 if error occurs or no books found.
        
    Raises:
        Exception: If database query fails.
    """
    conn = get_db_connection()
    if conn is None:
        return 0
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM BOOK")
        count = cur.fetchone()[0]
        cur.close()
        return count
        
    except Exception as e:
        print("Error getting book count:", e)
        return 0
    finally:
        conn.close()
import os
import psycopg2

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.
    
    Uses environment variables for database configuration with fallback to default values.
    Handles connection errors by printing the error and returning None.
    
    Environment Variables:
        DB_HOST: Database host (default: 'localhost')
        DB_NAME: Database name (default: 'lms')
        DB_USER: Database user (default: 'postgres')
        DB_PASSWORD: Database password (default: 'postgreSem')
        DB_PORT: Database port (default: '5432')
    
    Returns:
        psycopg2.connection: Database connection object if successful
        None: If connection fails
    
    Raises:
        Prints connection errors but does not propagate exceptions
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'lms'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgreSem'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None