from connect import get_connection
def insert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    # SQL query to add a row
    sql = "INSERT INTO contacts (username, phone_number) VALUES (%s, %s);"
    cur.execute(sql, (name, phone))
    conn.commit() # Critical: This saves the changes!
    cur.close()
    conn.close()

def search_contact(pattern):
    conn = get_connection()
    cur = conn.cursor()
    # Using 'LIKE' for pattern matching (e.g., name starts with 'A')
    sql = "SELECT * FROM contacts WHERE username LIKE %s;"
    cur.execute(sql, (pattern + '%',))
    results = cur.fetchall()
    for row in results:
        print(row)
    cur.close()
    conn.close() 
