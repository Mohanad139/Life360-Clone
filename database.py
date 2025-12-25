import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations(
            user_id TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            timestamp TEXT)
                   """)
    
    conn.commit()
    conn.close()

def insert_location(user_id, lat, lon):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")   
    
    cursor.execute("""
        INSERT INTO locations VALUES (?,?,?,?)       
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

def update_location(user_id,lat,lon):
    #Connect to The database
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()
    #Get The timming
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")   
    #Update the table of the user
    cursor.execute("""
        UPDATE locations
        SET latitude = ?, longitude = ?, timestamp = ?
        WHERE user_id = ?           
    """,(lat,lon,timestamp,user_id,))

    conn.commit()
    conn.close()


