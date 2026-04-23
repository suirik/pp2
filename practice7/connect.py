import psycopg2 
from config import host, database, user, password

def get_connection():
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None 
