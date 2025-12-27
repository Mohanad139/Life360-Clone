import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def insert_location(user_id, lat, lon):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")   

    cursor.execute("""
        INSERT INTO locations (user_id,latitude,longitude,timestamp) VALUES (?,?,?,?)       
    """,(user_id,lat,lon,timestamp))
    conn.commit()
    conn.close()


def gets_location(user_id):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM locations
        WHERE user_id = ?
        ORDER BY timestamp DESC LIMIT 1
                    """,(user_id,))
    
    row = cursor.fetchone()

    conn.close()
    return row
    

def get_all_locations():
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM locations
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_location(user_id):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM locations
        WHERE user_id = ?      
            """,(user_id,))
    
    conn.commit()
    conn.close()




def get_user_history(user_id):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM locations
        WHERE user_id = ?
        ORDER BY timestamp DESC      
        """,(user_id,))
    
    row = cursor.fetchall()

    conn.close()
    return row

def create_users_table():
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT)
            """)
    
    conn.commit()
    conn.close()

def insert_users_table(username,password_hash):
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO users (username,password_hash,created_at) VALUES (?,?,?)  
        """,(username,password_hash,timestamp))
    
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    cursor.execute("""
      SELECT *
      FROM users
      WHERE username = ?             
    """,(username,))

    row = cursor.fetchone()
    conn.close()
    return row




