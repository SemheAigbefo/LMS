import psycopg2
from psycopg2 import OperationalError

def connect_to_postgres():
    """Connect to PostgreSQL database"""
    try:

        connection = psycopg2.connect(
            host='localhost',          
            database='postgres',    
            user='postgres',         
            password='postgreSem',  
            port='5432'                
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