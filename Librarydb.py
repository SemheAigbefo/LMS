import psycopg2

# First, create the database if it doesn't exist
def create_database():
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

# Database connection function - MODIFIED to connect to lms database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",       
            database="lms",  # Changed to connect to your lms database
            user="postgres",
            password="postgreSem",
            port=5432
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# Initialize database tables
def init_database():
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        cur = conn.cursor()
        # Create tables if they don't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS LIBRARIAN (
                name TEXT,
                id INT PRIMARY KEY
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS BOOK (
                name TEXT,
                ISBN BIGINT PRIMARY KEY,
                Author TEXT,
                Pub_Year INT,
                Availability TEXT DEFAULT 'Available'
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS L_MEMBER (
                name TEXT,
                ID INT PRIMARY KEY,
                contact TEXT
            );
        """)
        
        # Insert sample data
        cur.execute("""
            INSERT INTO LIBRARIAN (name, id) VALUES
            ('Alice Johnson', 70895),
            ('Ben Carter', 70704),
            ('Chloe Smith', 70552)
            ON CONFLICT (id) DO NOTHING;
        """)
        
        cur.execute("""
            INSERT INTO L_MEMBER (name, ID, contact) VALUES
            ('Daniel Lee', 101, 'daniel.lee@example.com'),
            ('Emma Davis', 102, 'emma.davis@example.com'),
            ('Liam Brown', 103, 'liam.brown@example.com')
            ON CONFLICT (ID) DO NOTHING;
        """)
        
        conn.commit()
        cur.close()
        
    except Exception as e:
        print("Error initializing database:", e)
    finally:
        conn.close()

# Initialize the database when the module is imported
init_database()

# Database operations
def add_book_to_db(book):
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
    Get all books from the database
    Returns list of books or None if error
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
    Get total number of books in database
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