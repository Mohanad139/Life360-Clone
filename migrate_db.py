import sqlite3
import os

# Delete the old database
if os.path.exists('locations.db'):
    os.remove('locations.db')
    print("Old database deleted")

# Create new schema
conn = sqlite3.connect('locations.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        timestamp TEXT NOT NULL
    )
""")

conn.commit()
conn.close()
print("New database created with history support")