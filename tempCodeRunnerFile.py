ef verify_librarian_id(l_id):
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
