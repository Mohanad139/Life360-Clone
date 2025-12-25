import sqlite3

def init_db():
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations(
            User_id TEXT PRIMARY KEY,
            Latitude REAL,
            Longitude REAL,
            Timestamp TEXT)
                   """)
    
    conn.commit()
    conn.close()

def insert_location(user_id, lat, lon, timestamp):
    conn = sqlite3.connect("locations.db")
    cursor = conn.cursor()

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
