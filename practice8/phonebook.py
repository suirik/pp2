from connect import connect

def add_contact(name, phone):
    conn = connect()
    if conn:
        cur = conn.cursor()
        # Calling a Stored Procedure uses .execute("CALL ...")
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print(f"Contact {name} processed.")
        cur.close()
        conn.close()

def find_contacts(pattern):
    conn = connect()
    if conn:
        cur = conn.cursor()
        # Calling a Function uses .execute("SELECT * FROM ...")
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
        rows = cur.fetchall()
        for row in rows:
            print(f"Name: {row[0]}, Phone: {row[1]}")
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Test your code here
    add_contact('Aleksey', '87071112233')
    find_contacts('Aleks')
