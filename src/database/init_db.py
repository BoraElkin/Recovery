import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from connection import engine, Base

def create_database():
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        user="boraelkin",
        password="recproject1905",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create a cursor
    cur = conn.cursor()
    
    try:
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'recovery_db'")
        exists = cur.fetchone()
        
        if not exists:
            # Create database
            cur.execute('CREATE DATABASE recovery_db')
            print("Database created successfully!")
        else:
            print("Database already exists!")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

def init_tables():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")

if __name__ == "__main__":
    create_database()
    init_tables() 