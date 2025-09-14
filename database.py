import psycopg2
from psycopg2 import OperationalError

def connect_to_postgres():
    """Connect to PostgreSQL database"""
    try:
        # Connection parameters - MUST match your PostgreSQL setup
        connection = psycopg2.connect(
            host='localhost',          # or '127.0.0.1'
            database='postgres',       # Default database
            user='postgres',           # Default username
            password='postgreSem',  # ⚠️ CHANGE THIS to your actual password
            port='5432'                # Default PostgreSQL port
        )
        
        print("✅ Successfully connected to PostgreSQL from VSCode!")
        return connection
        
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return None

# Test the connection
if __name__ == "__main__":
    conn = connect_to_postgres()
    if conn:
        conn.close()